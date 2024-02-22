from bardapi import Bard
api_key = "dQiSoceNhHzhcsxlXXG01kZlUejI1IgBLM_sm9J2so72rWUIzINxPBaCLKYZge-SllrOjg."
token = api_key
bard = Bard(token=token)
a = bard.get_answer("Give an awsome knowledge graph for \"finding sum of elements an array in one loop \".Create small,precise,accurate and logically correct knowledge graph and give me a dot file. Make sure the dot file does not content any syntax error. Output only the cross verified dot file. I excpet just the dot file and no other text from you")['content']
with open("graph.dot","w") as file_obj:
    file_obj.write(a)
import pydot
(graph,) = pydot.graph_from_dot_file('graph.dot')
graph.write_png('graph.png')