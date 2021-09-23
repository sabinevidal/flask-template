"""Compile static assets."""
from flask import current_app as app
from flask_assets import Bundle

def compile_static_assets(assets):
    """Create stylesheet bundles."""
    assets.auto_build = True
    assets.debug = False
    css = Bundle('src/style.css',
                filters='postcss',
                output='dist/main.css')
    # common_style_bundle = Bundle(
    #     'src/less/*.less',
    #     filters='less,cssmin',
    #     output='dist/css/style.css',
    #     extra={'rel': 'stylesheet/less'}
    # )
    # home_style_bundle = Bundle(
    #     'home_bp/less/home.less',
    #     filters='less,cssmin',
    #     output='dist/css/home.css',
    #     extra={'rel': 'stylesheet/less'}
    # )
    # example_style_bundle = Bundle(
    #     'example_bp/less/example.less',    # Set static path within blueprint
    #     filters='less,cssmin',
    #     output='dist/css/example.css',
    #     extra={'rel': 'stylesheet/less'}
    # )
    assets.register('main_css', css)
    # assets.register('common_style_bundle', common_style_bundle)
    # assets.register('home_style_bundle', home_style_bundle)
    # assets.register('home_style_bundle', example_style_bundle)
    if app.config['FLASK_ENV'] == 'development':
        css.build()
        # common_style_bundle.build()
        # home_style_bundle.build()
        # example_style_bundle.build()
    return assets