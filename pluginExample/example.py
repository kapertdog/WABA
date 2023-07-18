import waba.plugin
import moduleOfExample

info = waba.plugin.Info(
    path="exampleVersionInfo.json"
)

example = waba.plugin.Plugin(
    name="Example",
    info=info,
)

settingsTree = waba.plugin.SettingsTree(example)
settingsTree.attach(moduleOfExample.moduleFolder)
