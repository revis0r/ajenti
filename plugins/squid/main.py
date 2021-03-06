from ajenti.ui import *
from ajenti.com import implements
from ajenti.app.api import ICategoryProvider
from ajenti.app.helpers import CategoryPlugin, ModuleContent, EventProcessor, event

from ajenti import apis
from backend import *

class SquidContent(ModuleContent):
    module = 'squid'
    path = __file__


class SquidPlugin(CategoryPlugin):
    implements((ICategoryProvider, 70))

    text = 'Squid'
    icon = '/dl/squid/icon.png'
    platform = ['Debian', 'Ubuntu']

    def on_init(self):
        self._parts = sorted(self.app.grab_plugins(apis.squid.IPluginPart),
                             key=lambda x: x.weight)
        
        idx = 0
        for p in self._parts:
            p.init(self, self._cfg, idx)
            idx += 1
                
    def on_session_start(self):
        self._tab = 0
        self._cfg = SquidConfig()
        self._cfg.load()
        
    def get_ui(self):
        status = 'is running' if is_running() else 'is stopped';
        panel = UI.PluginPanel(UI.Label(text=status), title='Squid Proxy Server', icon='/dl/squid/icon.png')

        if not is_installed():
            panel.appendChild(UI.VContainer(UI.ErrorBox(title='Error', text='Squid is not installed')))
        else:
            panel.appendChild(self.get_default_ui())        

        return panel


    def get_default_ui(self):
        tc = UI.TabControl(active=self._tab)
        for p in self._parts:
            tc.add(p.title, p.get_ui())
        return tc


    
    @event('button/click')
    def on_click(self, event, params, vars=None):
        for p in self._parts:
            p.on_click(event, params, vars)
            
    @event('dialog/submit')
    @event('form/submit')
    def on_submit(self, event, params, vars=None):
        for p in self._parts:
            p.on_submit(event, params, vars)

  
