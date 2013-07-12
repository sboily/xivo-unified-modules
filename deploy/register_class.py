def registerclass(server):
        exec("from app.plugins.%s.deploy_%s import %s" %(server.name.lower(), server.name.lower(), server.classname))
        cls = eval(server.classname)()

        return cls
