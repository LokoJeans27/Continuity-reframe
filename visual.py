"""Generate a visual canvas from the executed API graph without losing autogrow links."""
import copy

def normalize(name):
    return name.replace('ref_image_1','ref_image_0').replace('ref_video_1','ref_video_0').replace('ref_video_audio_1','ref_video_audio_0')

def make_visual(api,template):
    ui=copy.deepcopy(template); nodes={str(n['id']):n for n in ui['nodes']}
    if set(nodes)!=set(api):raise ValueError('Visual template and API node sets differ')
    for key,item in api.items():
        n=nodes[key]
        if n['type']!=item['class_type']:raise ValueError('Node type mismatch')
        named=n.get('widgets_values_named',{})
        # The frontend export preserves named insertion order matching positional widgets.
        for name,value in item['inputs'].items():
            if isinstance(value,list):continue
            if name not in named:raise ValueError('Unknown widget '+key+':'+name)
            pos=list(named).index(name)
            n['widgets_values'][pos]=value;named[name]=value
    errors=verify_visual(api,ui)
    if errors:raise ValueError(errors)
    return ui

def verify_visual(api,ui):
    nodes={str(n['id']):n for n in ui['nodes']};links={x[0]:x for x in ui['links']};errors=[]
    for key,n in api.items():
        visual=nodes[key];inputs={x['name']:x for x in visual['inputs']};widgets=visual.get('widgets_values_named',{})
        for name,value in n['inputs'].items():
            if isinstance(value,list):
                item=inputs.get(normalize(name));link=links.get(item.get('link')) if item else None
                if not link or [str(link[1]),link[2]]!=value:errors.append([key,name,'link_mismatch'])
                elif link[0] not in (nodes[str(link[1])]['outputs'][link[2]].get('links') or []):errors.append([key,name,'reverse_link_missing'])
            elif widgets.get(name)!=value or visual['widgets_values'][list(widgets).index(name)]!=value:errors.append([key,name,'widget_mismatch'])
    return errors
