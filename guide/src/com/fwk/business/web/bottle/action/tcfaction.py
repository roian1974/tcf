from src.com.fwk.business.util.reflection import reflection

def action(service,program,data1,data2) :

    argv = ['tcf_sp_commo',service,program,data1,data2]
    res = reflection.reflection_argv('src.com.fwk.business.tcf.tcf_sp_commo', 'main',argv)
    return res
