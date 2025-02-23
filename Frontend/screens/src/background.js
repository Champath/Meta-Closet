chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "tryOnImage",
      title: "Try On This Image",
      contexts: ["image"]
    });
  });
  
  chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === "tryOnImage") {
      chrome.storage.local.set({ uploadedImage: info.srcUrl }, () => {
        chrome.action.openPopup();
      });
    }
  });
  