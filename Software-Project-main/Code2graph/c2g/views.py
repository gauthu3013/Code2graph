from django.shortcuts import render, redirect
import os
from bardapi import Bard
from django.template import Node, TemplateSyntaxError
from django.core.files.storage import FileSystemStorage
import pydot
from django.conf import Settings
from Code2graph import settings
api = ""
disp_api = ""
def home_view(request):
    global api,disp_api
    api=""
    if request.method == 'POST':
        api = request.POST.get('api', '')
        disp_api= "*" * 5 + api[:5]
        return redirect('convert/') 
    return render(request, "c2g/enterapi.html")
def getting(request):
    global api,disp_api
    if request.method == 'POST':
        if "codefile" in request.FILES:
            file = request.FILES['codefile']
            text = file.read()
            text = text.decode()
            print(f"The QUERY Raised by the user is the file with name : {file}")
            return get_graph_file(request,text)
        else:
            print(f"The QUERY Raised by the user : {request.POST['req']}")
            return get_graph_file(request, request.POST['req'])
    ren = {'api_key': disp_api}
    return render(request, "c2g/Getting.html", ren)
def get_graph_file(request, text):
    print("-------------------------------------- DISPLAYING QUERY LOG --------------------------------------")
    global disp_api,api
    code = prompt_engineer(text)
    flag,code = get_graph(code)
    if code=="apierror":
        return redirect('apierror')
    return render(request=request, template_name="c2g/output.html",
                context={'api_key':disp_api,'code':code,'flag':flag})
def get_graph(text):
    try:
        bard = Bard(token=api)
        a = bard.get_answer(text)['content'].split("```")[1]
        a = a.lstrip("dot")
        print("Writing file")
        print()
        import os
        base_dir = str(settings.BASE_DIR)
        static_url = settings.STATIC_URL
        generated_dir = "generated"
        full_path = os.path.join(base_dir, "c2g", static_url, generated_dir)
        dot_file_path = os.path.join(full_path, "graph.dot")
        png_file_path = os.path.join(full_path, "graph1.png")
        with open(dot_file_path,"w") as file_obj:
            file_obj.write(a)
            print("Writing complete!!")
            print()
        print("Displaying the response from Bard")
        print()
        print(a)
        try:
            print("Writing into a picture")
            (graph,) = pydot.graph_from_dot_file(dot_file_path)
            print("Read from the graph file completely!!!")
            graph.write_png(png_file_path)
            print()
            print("-------------------------------------- SUCCESSFUL EXECUTION --------------------------------------")
            return True,a      
        except Exception as E:
            print(E)
            print()
            print("-------------------------------------- UNSUCCESSFUL EXECUTION --------------------------------------")
            return False,"gpterror"
    except Exception as e:
        print(e)
        return False,"apierror"
def prompt_engineer(text):
    return f'''Give a logic knowledge graph for "+{text}+" 
              Create 'small','precise','accurate' and 'logically correct' knowledge graph and
              give me a correct dot file with 'proper syntax' and 'proper shapes' inside the graph .
              Make sure the dot file does not content any syntax error. 
              I only expect the corss verified code from you and nothing else.'''
def apierror(request):
    global api,disp_api
    if request.method=="POST":
        api = request.POST.get('api', '')
        disp_api= "*" * 5 + api[:5]
        return redirect('input veiw')
    return render(request,"c2g/apierror.html")