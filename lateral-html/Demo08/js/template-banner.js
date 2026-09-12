(function () {
	var STORAGE_KEY = "qmTemplateBannerDismissed";
	var banner = document.querySelector(".template-banner");
	var closeButton = document.querySelector("[data-template-banner-close]");
	var downloadLink = document.querySelector("[data-template-download]");

	function dismiss() {
		document.documentElement.classList.remove("has-template-banner");
		try {
			localStorage.setItem(STORAGE_KEY, "1");
		} catch (error) {
			/* ignore quota / private mode */
		}
		if (banner) {
			banner.setAttribute("hidden", "hidden");
		}
	}

	if (!document.documentElement.classList.contains("has-template-banner")) {
		if (banner) {
			banner.setAttribute("hidden", "hidden");
		}
		return;
	}

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
