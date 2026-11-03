from pathlib import Path
import base64, hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile, time
from urllib.request import build_opener, ProxyHandler, Request
from urllib.parse import quote
try:
    from playwright.sync_api import sync_playwright, expect
except ImportError:
    raise SystemExit('Install maintenance dependencies: python -m pip install -r requirements-dev.txt')
root=Path(__file__).resolve().parent.parent
if os.name != 'nt':
    raise SystemExit('This browser smoke test currently targets Windows with installed Microsoft Edge.')
qa=root/'.test-artifacts'
qa.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('install_e2e',root/'scripts/initialize.py')
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
opener=build_opener(ProxyHandler({}))
with tempfile.TemporaryDirectory(prefix='pm-full-check-',dir=qa) as directory:
    project=Path(directory).resolve();assert project.is_relative_to(qa.resolve())
    shutil.copytree(root/'examples/favorites',project,dirs_exist_ok=True)
    installer.install(project,quiet=True,with_launcher=False)
    appdata=project/'test-system'
    (appdata/'pm-workflow').mkdir(parents=True)
    (appdata/'pm-workflow/state.json').write_text(json.dumps({'engine':'msedge'}),encoding='utf-8')
    env=os.environ.copy();env.update(PROTOTYPE_PROJECT_DIR=str(project),LOCALAPPDATA=str(appdata),PM_OPEN_BROWSER='0',PYTHONUTF8='1')
    log=(project/'service-test.log').open('w',encoding='utf-8')
    service=subprocess.Popen([sys.executable,str(project/'scripts/prototype_server.py')],env=env,stdout=log,stderr=subprocess.STDOUT)
    try:
        for _ in range(100):
            config=json.loads((project/'.pm-workflow/runtime.json').read_text(encoding='utf-8'))
            base='http://127.0.0.1:'+str(config['port'])
            try:
                with opener.open(base+'/api/health',timeout=1) as response:
                    assert json.load(response)['project_id']==config['project_id']
                break
            except Exception:
                if service.poll() is not None: raise RuntimeError((project/'service-test.log').read_text(encoding='utf-8'))
                time.sleep(.1)
        else: raise RuntimeError('Service did not become ready')
        def post(endpoint,payload,authorized=True):
            headers={'Content-Type':'application/json','Origin':base}
            if authorized: headers.update({'X-PM-Project':config['project_id'],'X-PM-Token':config['token']})
            request=Request(base+endpoint,data=json.dumps(payload).encode(),headers=headers,method='POST')
            with opener.open(request,timeout=40) as response:return json.load(response)
        prototype='/收藏功能/原型/收藏功能-prototype.html'
        document='/收藏功能/需求文档/收藏功能-PRD.html'
        errors=[]
        with sync_playwright() as p:
            browser=p.chromium.launch(channel='msedge',headless=True)
            context=browser.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'])
            page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto(base+quote(prototype)+'#all')
            page.get_by_role('button',name='收藏 产品需求分析',exact=True).click()
            page.get_by_role('link',name='我的收藏',exact=True).click()
            expect(page.locator('#favorite-courses article')).to_have_count(1)
            page.get_by_role('button',name='模拟下次操作失败').click()
            page.get_by_role('button',name='取消收藏 产品需求分析',exact=True).click()
            expect(page.locator('#favorite-courses article')).to_have_count(1)
            expect(page.locator('#notice')).to_contain_text('失败')
            page.get_by_role('button',name='取消收藏 产品需求分析',exact=True).click()
            expect(page.locator('#empty')).to_be_visible()
            page.goto(base+quote(document))
            page.wait_for_function('revisionReady')
            assert page.locator('#dock').get_attribute('src') is None
            page.get_by_role('button',name='双栏预览',exact=True).click()
            expect(page.locator('#sidebar')).to_be_visible()
            page.locator('#page').select_option('favorites')
            expect(page.frame_locator('#dock').get_by_role('heading',name='我的收藏',exact=True)).to_be_visible()
            page.locator('#plus').click();expect(page.locator('#zoom')).to_have_text('110%')
            page.get_by_role('button',name='收起预览',exact=True).click()
            cell=page.locator('.meta-table tbody tr').first.locator('td').nth(1)
            before=cell.inner_text();cell.fill('课程收藏·编辑验证');page.locator('header strong').click()
            page.get_by_role('button',name='撤销',exact=True).click();expect(cell).to_have_text(before)
            page.get_by_role('button',name='重做',exact=True).click();expect(cell).to_have_text('课程收藏·编辑验证')
            rows=page.locator('.version-table tbody tr')
            rows.first.hover();rows.first.locator('.row-add').click();expect(rows).to_have_count(2)
            rows.last.hover();rows.last.locator('.row-del').click();expect(rows).to_have_count(1)
            page.get_by_role('button',name='撤销',exact=True).click();expect(rows).to_have_count(2)
            rows.last.hover();rows.last.locator('.row-add').click();expect(rows).to_have_count(3)
            page.get_by_role('button',name='撤销',exact=True).click();expect(rows).to_have_count(2)
            rows.last.hover();rows.last.locator('.row-del').click();expect(rows).to_have_count(1)
            wrap=page.locator('.overview-table').locator('..')
            wrap.hover();wrap.locator('.editable-table-remove').click();expect(page.locator('.overview-table')).to_have_count(0)
            page.get_by_role('button',name='撤销',exact=True).click();expect(page.locator('.overview-table')).to_have_count(1)
            # Resize controls operate on actual geometry and participate in undo.
            handle=page.locator('.version-table th .col-resizer').first
            handle.scroll_into_view_if_needed();box=handle.bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
            col=page.locator('.version-table col').first
            old_width=col.evaluate('(el)=>el.style.width')
            page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+40,y);page.mouse.up()
            assert col.evaluate('(el)=>el.style.width')!=old_width
            page.get_by_role('button',name='撤销',exact=True).click();assert col.evaluate('(el)=>el.style.width')==old_width
            row=rows.first;handle=row.locator('.row-resizer');handle.scroll_into_view_if_needed();box=handle.bounding_box();x=box['x']+20;y=box['y']+box['height']/2
            old_height=row.evaluate('(el)=>el.style.height')
            page.mouse.move(x,y);page.mouse.down();page.mouse.move(x,y+30);page.mouse.up();assert row.evaluate('(el)=>el.style.height')!=old_height
            page.get_by_role('button',name='撤销',exact=True).click();assert row.evaluate('(el)=>el.style.height')==old_height
            page.get_by_role('button',name='保存文档',exact=True).click();expect(page.locator('#status')).to_contain_text('已保存',timeout=15000)
            path=project/document.lstrip('/')
            assert '课程收藏·编辑验证' in path.read_text(encoding='utf-8')
            page.reload();page.wait_for_function('revisionReady')
            page.locator('.version-table tbody tr').first.hover();page.locator('.version-table tbody tr').first.locator('.row-add').click()
            expect(page.locator('.version-table tbody tr')).to_have_count(2)
            page.get_by_role('button',name='撤销',exact=True).click();expect(page.locator('.version-table tbody tr')).to_have_count(1)
            # Service snapshot is actual PNG output and then a cache hit.
            payload={'src':prototype+'#all','scale':2}
            first=post('/api/snapshot',payload);assert first['ok']
            assert base64.b64decode(first['dataUrl'].split(',',1)[1]).startswith(b'\x89PNG\r\n\x1a\n')
            assert Path(first['file']).is_file()
            second=post('/api/snapshot',payload);assert second['cached']
            page.get_by_role('button',name='复制全文',exact=True).click();expect(page.locator('#status')).to_have_text('已复制全文，包含原型图片。',timeout=40000)
            copied=page.evaluate("async()=>{for(const item of await navigator.clipboard.read())if(item.types.includes('text/html'))return await(await item.getType('text/html')).text()}")
            assert 'data:image/png;base64,' in copied and 'class="row-ctrl"' not in copied and 'contenteditable=' not in copied
            raw=path.read_bytes()
            from urllib.error import HTTPError
            try:post('/api/save-html',{'path':document,'content':'<!doctype html><html>stale</html>','revision':'wrong'})
            except HTTPError as error:assert error.code==409
            else:raise AssertionError('Stale save accepted')
            assert path.read_bytes()==raw
            page.goto(base+quote(document));page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(qa/'pm-full-prd.png'),full_page=True)
            page.goto(base+quote(prototype));page.set_viewport_size({'width':375,'height':860});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.screenshot(path=str(qa/'pm-full-prototype.png'),full_page=True)
            page.set_viewport_size({'width':1400,'height':480});page.goto((root/'assets/readme/cover.svg').as_uri());page.screenshot(path=str(qa/'pm-full-cover.png'))
            assert not errors,errors
            browser.close()
        print('PASS: real prototype behavior, preview laziness/navigation/zoom, text undo/redo, row/table restore, resize undo, save/reopen controls, PNG snapshot/cache, clipboard with inline images, revision conflict and 375px prototype layout.')
    finally:
        service.terminate()
        try:service.wait(timeout=10)
        except subprocess.TimeoutExpired:service.kill();service.wait()
        log.close()
