
import sys

if sys.platform == 'win32':
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

if sys.platform in ['darwin', 'linux']:
    from cx_Freeze import setup, Executable

    build_options = {
        "include_files" : ['images']
    }

    setup(
        data_files = [('images', ['images/rewave_app_icon.png'])],
        name = "Rewave Server",
        version = "0.0.1",
        description = "Rewave App's Server",
        executables = [Executable("rewave_server.pyw")],
        options = dict(build_exe = build_options),
        icon="images/rewave_app_icon.ico"
    )