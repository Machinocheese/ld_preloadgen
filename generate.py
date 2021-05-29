def last_nonalpha(string):
    retval = 0
    for i in range(len(string)):
        if string[i] == ' ':
            retval = i
        elif string[i] == '*':
            retval = i + 1

    return retval

def retrieve_format_string(vartype):
    if 'char *' in vartype:
        return '%s'
    elif 'char' in vartype:
        return '%c'
    else:
        return '%x'

def parse_declaration(info):
    retval = ""
    func_name = ""
    parameters = ""


    first_half = info[:info.find("(")]
    split = last_nonalpha(first_half)

    retval = first_half[:split].strip()
    func_name = first_half[split:].strip()


    params = info[info.find("(") + 1:info.find(")")]
    param_type = "("
    var_names = []
    for param in params.split(","):
        split = last_nonalpha(param)
        
        typed = param[:split].strip()
        var_names.append((typed, param[split:].strip()))
        param_type += " " + typed + ","

    param_type = param_type[:-1] + " )"
    return {'retval': retval,
            'func_name': func_name,
            'parameters': "(" + params + ")",
            'param_type': param_type,
            'variables': var_names,
            }
    #func_name = # going from '(' backwards, keep going until you either hit a non-letter char
    #print(params)

output="""#include <dlfcn.h>
#include <stdio.h>

#ifndef RTLD_NEXT
#define RTLD_NEXT ((void *) -1l)
#endif

"""

header = "int strncmp(const char *s1, const char *s2, size_t n);"
result = parse_declaration(header)

func_var = "func_" + result['func_name'] + ""

output += result['retval'] + " " + result['func_name'] + result['parameters'] + "{\n\n"
output += "  static " + result['retval'] + " (*" + func_var + ") " + result['param_type'] + " = NULL;\n"
output += "  if (!" + func_var + "){\n"
output += "    " + func_var + " = " + "(" + result['retval'] + " (*) " + result['param_type'] + ") dlsym(RTLD_NEXT, \"" + result['func_name'] + "\");\n  }\n"
output += "  " + result['retval'] + " retval = " + func_var + "("
for var in result['variables']:
    output += " " + var[1] + ","

output = output[:-1] + ");\n"
output += "  printf(\"" + result['func_name'] + "("
for var in result['variables']:
    format_string = retrieve_format_string(var[0])
    output += " " + format_string + ","

output = output[:-1] + ") = %x\", "
for var in result['variables']:
    output += "" + var[1] + ", "
output += "retval);\n"

# )\");\n"

output += "  return retval;\n}"

print(output)
