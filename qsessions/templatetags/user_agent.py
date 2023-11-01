from django import template
from django.utils.translation import gettext_lazy as _


register = template.Library()

@register.simple_tag(name="ua_str")
def ua_str(ua, include_os=False, include_versions=False):
	browser = ua_browser(ua.browser, include_version=include_versions)
	os = ua_os(ua.os, include_version=include_versions) if include_os else None
	device = ua_device(ua.device)
	if include_os and browser and os and device:
		return _("{browser} on {os}, {device}").format(
			browser=browser,
			os=os,
			device=device,
		)
	elif browser and device:
		return _("{browser} on {device}").format(
			browser=browser,
			device=device,
		)
	elif browser:
		return browser
	elif device:
		return device
	elif include_os and os:
		return os
	return None


@register.simple_tag(name="ua_browser")
def ua_browser(ua_browser, include_version=False):
	if include_version and ua_browser.version_string:
		return _("{browser} {version}").format(
			browser=ua_browser.family,
			version=ua_browser.version_string,
		)
	elif ua_browser.family:
		return ua_browser.family
	return None


@register.simple_tag(name="ua_os")
def ua_os(ua_os, include_version=False):
	if include_version and ua_os.version_string:
		return _("{os} {version}").format(
			os=ua_os.family,
			version=ua_os.version_string
		)
	elif ua_os.family:
		return ua_os.family
	return None


@register.simple_tag(name="ua_device")
def ua_device(ua_device):
	if ua_device.brand and ua_device.model:
		return _("{brand} {model}").format(
			brand=ua_device.brand,
			model=ua_device.model,
		)
	if ua_device.family:
		return ua_device.family
	return None
