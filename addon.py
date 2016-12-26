# bsl, 2016
import xbmc
import xbmcaddon
import json
import sys

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

REMOTE_DBG = False

if REMOTE_DBG:
	try:
		import pydevd
		pydevd.settrace(stdoutToServer=True, stderrToServer=True)
	except:
		xbmcgui.Dialog().ok(addonname, "debug mode not workng")
		sys.exit(1)


req =  xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettings","id":1}')

jsonRPCRes = json.loads(req);
settingsList = jsonRPCRes["result"]["settings"]

audioSetting =  [item for item in settingsList if item["id"] ==  "audiooutput.audiodevice"][0]
audioDeviceOptions = audioSetting["options"];
activeAudioDeviceValue = audioSetting["value"];

activeAudioDeviceId = [index for (index, option) in enumerate(audioDeviceOptions) if option["value"] == activeAudioDeviceValue][0];

nextIndex = ( activeAudioDeviceId + 1 ) % len(audioDeviceOptions)

nextValue = audioDeviceOptions[nextIndex]["value"]
nextName = audioDeviceOptions[nextIndex]["label"]

changeReq =  xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"audiooutput.audiodevice","value":"%s"},"id":1}' % nextValue)

try:
	changeResJson = json.loads(changeReq);

	if changeResJson["result"] != True:
		raise Exception
except:
	sys.stderr.write("Error switching audio output device")
	raise Exception

xbmc.executebuiltin('Notification("%s","Output-Device: %s",2000,"%s")' % (__addonname__, nextName, __icon__ ))



