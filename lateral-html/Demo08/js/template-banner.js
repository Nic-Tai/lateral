(function () {
	var STORAGE_KEY = "qmTemplateBannerDismissed";
	var root = document.documentElement;
	var banner = document.querySelector(".template-banner");
	var closeButton = document.querySelector("[data-template-banner-close]");
	var downloadLink = document.querySelector("[data-template-download]");

	function syncBannerHeight() {
		if (!banner || !root.classList.contains("has-template-banner") || banner.hasAttribute("hidden")) {
			root.style.setProperty("--template-banner-height", "0px");
			return;
		}
		root.style.setProperty("--template-banner-height", banner.offsetHeight + "px");
	}

	function dismiss() {
		root.classList.remove("has-template-banner");
		root.style.setProperty("--template-banner-height", "0px");
		try {
			localStorage.setItem(STORAGE_KEY, "1");
		} catch (error) {
			/* ignore quota / private mode */
		}
		if (banner) {
			banner.setAttribute("hidden", "hidden");
		}
	}

	if (!root.classList.contains("has-template-banner")) {
		if (banner) {
			banner.setAttribute("hidden", "hidden");
		}
		syncBannerHeight();
		return;
	}

	syncBannerHeight();
	if (window.ResizeObserver && banner) {
		new ResizeObserver(syncBannerHeight).observe(banner);
	}
	window.addEventListener("resize", syncBannerHeight);

	if (closeButton) {
		closeButton.addEventListener("click", function (event) {
			event.preventDefault();
			dismiss();
		});
	}

	if (downloadLink) {
		downloadLink.addEventListener("click", function () {
			downloadLink.classList.add("is-downloading");
		});
	}
})();
