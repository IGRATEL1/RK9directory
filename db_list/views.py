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

def material_detail2(request, id):
    try:
        material = Materials_stats.published.get(id=id)
        plots = [plot1(material),plot2(material)]
    except Materials_stats.DoesNotExist:
        raise Http404("NETYYY")
    return render(request, 'db_list/material/detail2.html',context={'material':material,'plots':plots})

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
        x_data=np.arange(100)/100
        y_data=float(material.yield_strength)+float(material.ludwig_const)*(x_data**float(material.material_hardening_index))
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', line_shape='spline'))
        fig.update_layout(autosize=False, width=500, height=500,paper_bgcolor="White", title="Кривая упрочнения")
        fig.update_yaxes(title="σ, МПа")
        fig.update_xaxes(title="ε, %")
        plot_div = plot(fig,
                output_type='div')
        return plot_div
    except:
        return ''

def post_new(request):
    form = PostForm()
    return render(request, 'db_list/material/material_edit.html', {'form':form})

def download_file(request, id):
    material = get_object_or_404(Materials_stats, id=id)
    response = FileResponse(open(material.ansys_file.path,'rb'))
    response['Content-Disposition'] = f'attachment;filename="{material.ansys_file.name}"'
    return response