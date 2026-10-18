import glob
import io
from contextlib import redirect_stdout, redirect_stderr
from IPython.display import Video, display, clear_output
from typing import Type

def render_and_display_scene(scene_class: Type, width: str = "80%", force_render: bool = False):
    """
    Renders a Manim scene (if not already cached) and embeds the resulting MP4 
    cleanly inside a Jupyter Notebook cell.
    """
    scene_name = scene_class.__name__
    video_paths = glob.glob(f"**/1080p60/{scene_name}.mp4", recursive=True)

    if not video_paths or force_render:
        suppressed_stream = io.StringIO()
        with redirect_stdout(suppressed_stream), redirect_stderr(suppressed_stream):
            scene = scene_class()
            scene.render()
        clear_output()
        video_paths = glob.glob(f"**/1080p60/{scene_name}.mp4", recursive=True)

    if video_paths:
        display(Video(video_paths[0], embed=True, html_attributes=f'controls width="{width}"'))
    else:
        print(f"Error: Video file for '{scene_name}' could not be located.")