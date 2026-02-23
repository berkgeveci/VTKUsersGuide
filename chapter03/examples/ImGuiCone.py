import vtk
from imgui_bundle import imgui, immapp, hello_imgui

class VtkImGuiRenderer:
    def __init__(self):
        self.renderer = vtk.vtkRenderer()
        
        # 1. Setup Generic Window strictly for Offscreen Texture generation
        self.render_window = vtk.vtkGenericOpenGLRenderWindow()
        self.render_window.AddRenderer(self.renderer)
        
        self.render_window.SetOwnContext(False)
        self.render_window.SetOffScreenRendering(True)
        
        # 2. Setup Interactor
        self.interactor = vtk.vtkGenericRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.render_window)
        
        # FORCE TRACKBALL INTERACTION
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.interactor.SetInteractorStyle(style)
        
        # 3. VTK Pipeline
        # PROMOTED TO `self` SO WE CAN MODIFY IT LATER
        self.cone_source = vtk.vtkConeSource()
        self.cone_source.SetResolution(6) # Default starting resolution
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.cone_source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.renderer.AddActor(actor)
        self.renderer.SetBackground(0.15, 0.15, 0.2)
        
        # Safe Anti-Aliasing that macOS allows
        self.renderer.SetUseFXAA(True) 
        
        # 4. State tracking for smooth interaction
        self.is_interacting = False

    def init_vtk_context(self):
        self.render_window.SetMapped(True)
        self.render_window.SetIsCurrent(True)
        self.render_window.OpenGLInitContext()

    def render_frame(self, phys_width, phys_height):
        if phys_width <= 0 or phys_height <= 0:
            return None
        
        self.render_window.SetSize(int(phys_width), int(phys_height))
        self.render_window.Render()
        
        fbo = self.render_window.GetRenderFramebuffer()
        if fbo:
            tex = fbo.GetColorAttachmentAsTextureObject(0)
            if tex:
                return tex.GetHandle()
        
        return None

    def handle_input(self, pos, logical_size):
        io = imgui.get_io()
        is_hovered = imgui.is_window_hovered()

        # 1. Start interaction if clicked INSIDE the window
        if is_hovered and (imgui.is_mouse_clicked(0) or imgui.is_mouse_clicked(1)):
            self.is_interacting = True

        # 2. If we aren't hovered AND we aren't dragging, ignore the mouse
        if not is_hovered and not self.is_interacting:
            return
            
        dpi_scale = io.display_framebuffer_scale
        
        # 3. Translate coordinates (allows dragging outside the window safely!)
        rel_x = io.mouse_pos.x - pos.x
        rel_y = logical_size.y - (io.mouse_pos.y - pos.y)
        
        phys_x = int(rel_x * dpi_scale.x)
        phys_y = int(rel_y * dpi_scale.y)
        
        self.interactor.SetEventInformation(phys_x, phys_y, int(io.key_ctrl), int(io.key_shift))
        
        if imgui.is_mouse_clicked(0): self.interactor.LeftButtonPressEvent()
        elif imgui.is_mouse_released(0): self.interactor.LeftButtonReleaseEvent()
        if imgui.is_mouse_clicked(1): self.interactor.RightButtonPressEvent()
        elif imgui.is_mouse_released(1): self.interactor.RightButtonReleaseEvent()
            
        self.interactor.MouseMoveEvent()

        # 4. End the interaction when the button is released ANYWHERE
        if imgui.is_mouse_released(0) or imgui.is_mouse_released(1):
            self.is_interacting = False

# --- Main Application Setup ---
vtk_engine = VtkImGuiRenderer()

def gui():
    # 1. Grab the actual OS window boundaries
    viewport = imgui.get_main_viewport()
    imgui.set_next_window_pos(viewport.work_pos)
    imgui.set_next_window_size(viewport.work_size)
    
    # 2. Define flags to remove the title bar, borders, and prevent dragging
    flags = (
        imgui.WindowFlags_.no_decoration | 
        imgui.WindowFlags_.no_move | 
        imgui.WindowFlags_.no_saved_settings
    )
    
    # 3. Create the seamless fullscreen window
    imgui.begin("Main Application", p_open=None, flags=flags)
    
    # --- IMGUI CONTROLS ---
    current_res = vtk_engine.cone_source.GetResolution()
    changed, new_res = imgui.slider_int("Cone Resolution", current_res, 3, 50)
    if changed:
        vtk_engine.cone_source.SetResolution(new_res)
        
    imgui.separator()
    
    # --- VTK VIEWPORT ---
    # Get Logical Size for the REMAINING space (after the slider)
    logical_size = imgui.get_content_region_avail()
    pos = imgui.get_cursor_screen_pos()
    
    # Calculate Physical Size for VTK
    dpi_scale = imgui.get_io().display_framebuffer_scale
    phys_w = int(logical_size.x * dpi_scale.x)
    phys_h = int(logical_size.y * dpi_scale.y)

    # Process Interaction
    vtk_engine.handle_input(pos, logical_size)
    
    # Render and Retrieve Texture
    raw_tex_id = vtk_engine.render_frame(phys_w, phys_h)
    
    if raw_tex_id is not None:
        if hasattr(imgui, "ImTextureRef"):
            tex_obj = imgui.ImTextureRef(raw_tex_id)
        else:
            tex_obj = imgui.ImTextureID(raw_tex_id)
            
        # Display the texture
        imgui.image(
            tex_obj, 
            logical_size, 
            uv0=imgui.ImVec2(0, 1), 
            uv1=imgui.ImVec2(1, 0)
        )
    else:
        imgui.text("Waiting for VTK to generate texture...")
    
    imgui.end()

# --- Application Configuration ---
runner_params = hello_imgui.RunnerParams()
runner_params.callbacks.show_gui = gui
runner_params.callbacks.post_init = vtk_engine.init_vtk_context

# Give the OS window a title and a nice default starting size
runner_params.app_window_params.window_title = "VTK 9 + Dear ImGui"
runner_params.app_window_params.window_geometry.size = (1000, 800)

immapp.run(runner_params)