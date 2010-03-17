from plugin import PluginMaster, PluginInstance
import commands
import session
import ui
import log
import tools

class IptablesPluginMaster(PluginMaster):
	name = 'IPTables Firewall'

	def make_instance(self):
		i = IptablesPluginInstance(self)
		self.instances.append(i)
		return i


class IptablesPluginInstance(PluginInstance):
	name = 'IPTables Firewall'
	_lblUptime = None
	_actApply = None

	def _on_load(self, s):
		PluginInstance._on_load(self, s)

		c = ui.Category()
		c.text = 'Firewall'
		c.description = 'Manage IPTables'
		c.icon = 'plug/iptables;icon'
		self.category_item = c
		self.build_panel()
		log.info('IptablesPlugin', 'Started instance')

	def build_panel(self):
		self._lblUptime = ui.Label()
		l = ui.Label('IPTables management')
		l.size = 5

		self._actApply = ui.Action()
		self._actApply.text = 'Apply'
		self._actApply.description = 'Use saved configuration (iptables-restore)'
		self._actApply.icon = 'core;ui/icon-ok'
		self._actApply.handler = self._on_button_clicked

		c = ui.HContainer([ui.Image('plug/powermgmt;bigicon.png'), ui.Spacer(10,1), ui.VContainer([l, self._lblUptime])])
		d = ui.HContainer([self._actApply])
		self.panel = ui.VContainer([c, d])
		return


	def _on_button_clicked(self, t, e, d):
		return

	def Update(self):
		if self.panel.visible:
			self._lblUptime.text = '&nbsp;Uptime: ' + tools.actions['powermgmt/uptime-hms'].run()
		return


class UptimeAction(tools.Action):
	name = 'uptime'
	plugin = 'powermgmt'

	def run(self, d = None):
		return tools.actions['core/script-run'].run(['powermgmt', 'uptime', ''])

class UptimeHMSAction(tools.Action):
	name = 'uptime-hms'
	plugin = 'powermgmt'

	def run(self, d = None):
		s = int(tools.actions['core/script-run'].run(['powermgmt', 'uptime', '']))
		h = s / 3600
		m = s / 60 % 60
		s = s % 60
		return str(h) + ':' + str(m) + ':' + str(s)

class ShutdownAction(tools.Action):
	name = 'shutdown'
	plugin = 'powermgmt'

	def run(self, d = None):
		return tools.actions['core/script-run'].run(['powermgmt', 'shutdown', ''])

class RebootAction(tools.Action):
	name = 'reboot'
	plugin = 'powermgmt'

	def run(self, d = None):
		return tools.actions['core/script-run'].run(['powermgmt', 'reboot', ''])
