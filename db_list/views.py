from django.shortcuts import render
from .models import Materials_stats
from .forms import PostForm
from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
import os

from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
import plotly.express as px

import numpy as np

def material_list(request):
    materials = Materials_stats.published.all()
    return render(request, 'db_list/material/list.html',{'materials':materials})

def material_detail(request, id):
    try:
        material = Materials_stats.published.get(id=id)
        plots = [plot1(material),plot2(material)]
    except Materials_stats.DoesNotExist:
        raise Http404("NETYYY")
    return render(request, 'db_list/material/detail.html',context={'material':material,'plots':plots})

def plot1(material):
    try:
        data=np.loadtxt(material.graph_file)
        x_data=data[:,0]
        y_data=data[:,1]
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', line_shape='spline'))
        fig.update_layout(autosize=False, width=500, height=500,paper_bgcolor="LightSteelBlue",title="dddd")
        plot_div = plot(fig,
                output_type='div',title="plot")

        return plot_div
    except:
        return ''

def plot2(material):
    try:
        x_data=np.arange(10)/10
        y_data=float(material.yield_strength)+float(material.ludwig_const)*(x_data**float(material.material_hardening_index))
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', line_shape='spline'))
        fig.update_layout(autosize=False, width=500, height=500,paper_bgcolor="LightSteelBlue", title="Кривая упрочнения")
        fig.update_yaxes(title="σ, МПа")
        fig.update_xaxes(title="ε")
        plot_div = plot(fig,
                output_type='div')
        return plot_div
    except:
        return ''

def post_new(request):
    form = PostForm()
    return render(request, 'db_list/material/material_edit.html', {'form':form})

def download_file(request, material):
    file = get_object_or_404(material.ansys_file)
    file_path = material.ansys_file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename="{material.title}"'
    return response