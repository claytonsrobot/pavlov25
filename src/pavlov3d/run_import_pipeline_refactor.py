class PipelineState(dict):
    """Simple dict-based state container with attribute access."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__


class ImportPipeline:
    def __init__(self, scene, style, user_input, hierarchy):
        self.state = PipelineState(
            scene=scene,
            style=style,
            user_input=user_input,
            hierarchy=hierarchy,
        )

    def run(self):
        self._determine_plugins()
        self._run_import()
        self._normalize()
        self._populate_scene()
        self._prepare_exports()
        return self.state.export_control_object

    # ---- STAGES ----

    def _determine_plugins(self):
        self.state.user_input.determine_which_plugins_to_use()

    def _run_import(self):
        ImportPlugin = load_import_plugin_object(
            self.state.scene, self.state.style, self.state.user_input
        )
        importer = ImportPlugin()
        importer.run_import()
        self.state.importer = importer

    def _normalize(self):
        MultipleAxesScalingAlgorithm.normalize_all_curve_objects(
            set(self.state.hierarchy.dict_curve_objects_all.values())
        )
        self.state.style.calculate_halfwidths_and_directions()

    def _populate_scene(self):
        imp = self.state.importer
        self.state.scene.populate_basic_data(
            imp.names,
            imp.vectorArray_time,
            imp.vectorArray_height,
            imp.vectorArray_depth,
            imp.headers_time,
            imp.headers_height,
            imp.headers_depth,
        )
        messaging.print_data_range(self.state.scene)

    def _prepare_exports(self):
        export_plugins = self.state.style.prepare_export_modules()
        export_control = export_plugins[0]
        self.state.user_input.pull_values_from_export_control_object(export_control)
        TextTranslationIntermediate.assign_style_object(self.state.style)
        TextTranslationIntermediate.prepare_text()
        export_control.export_name = self.state.scene.filename_FBX
        self.state.export_control_object = export_control
