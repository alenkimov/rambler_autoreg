let hCaptchaInstance;

Object.defineProperty(window, "hcaptcha", {
  get: function () {
    return hCaptchaInstance;
  },
  set: function (e) {
    hCaptchaInstance = e;

    let originalRenderFunc = e.render;

    hCaptchaInstance.render = function (container, opts) {
      hCaptchaInstance.submit = opts.callback
      return originalRenderFunc(container, opts);
    };

    hCaptchaInstance.getResponse = function() {
      return document.querySelector('textarea[name="h-captcha-response"]').value || "";
    }
  },
});