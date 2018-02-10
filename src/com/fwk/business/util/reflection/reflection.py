def importer(name, root_package=False, relative_globals=None, level=0):

    return __import__(name, locals=None, # locals has no use
                      globals=relative_globals,
                      fromlist=[] if root_package else [None],
                      level=level)


def reflection(module_name,function_name) :
    module = importer(module_name)
    call = getattr(module,function_name)
    call()

def reflection_argv(module_name,function_name,argv) :
    module = importer(module_name)
    call = getattr(module,function_name)

    res = call(argv)
    return res

# relection('src.com.sp_commo.business.pc.sp_commo','SP_commo')


