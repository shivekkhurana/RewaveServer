from distutils.core import setup
import py2exe

setup(
	data_files = [('images', ['images/rewave_app_icon.png'])],
	windows = [{
		"script":"rewave_server.pyw",
		"icon_resources" : [(1, "images/rewave_app_icon.ico")],
		"dest_base" : "Rewave Server"
	}],
	options = {
		"py2exe" : {
			"optimize" : 2,
			"compressed" : 1
		}
	}
) 