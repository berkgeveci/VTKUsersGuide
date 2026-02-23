const cone = vtk.vtkConeSource();
await cone.setResolution(8);

const mapper = vtk.vtkPolyDataMapper();
await mapper.setInputConnection(await cone.getOutputPort());

const actor = vtk.vtkActor();
await actor.setMapper(mapper);

const renderer = vtk.vtkRenderer();
await renderer.addActor(actor);
await renderer.setBackground(0.2, 0.3, 0.4);
await renderer.resetCamera();

const canvasSelector = "#vtk-wasm-window";
const renderWindow = vtk.vtkRenderWindow({ canvasSelector });
await renderWindow.addRenderer(renderer);

const interactor = vtk.vtkRenderWindowInteractor({
  canvasSelector,
  renderWindow,
});
await interactor.interactorStyle.setCurrentStyleToTrackballCamera();

await interactor.start();
