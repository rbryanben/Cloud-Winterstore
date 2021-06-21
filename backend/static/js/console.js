//entry
window.document.addEventListener("readystatechange",()=>{
    var progress = document.querySelector(".loading-modal-body-bar-inner")
    switch (document.readyState) {
        case "interactive":
            // The document has finished loading. We can now access the DOM elements.
            // But sub-resources such as scripts, images, stylesheets and frames are still loading.
            if (!progress.classList.contains("second")){
                progress.classList.add("second")
            }
            break;
        case "complete":
            // The page is fully loaded.
            if (!progress.classList.contains("third")){
                progress.style.transition = "all 0.2s ease-in"
                progress.classList.add("third")
                setTimeout(hideConsoleLoading(),200)
            }
            break;
        }
})


//
//document
function disableScrolling() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function() { window.scrollTo(x, y); };
}



///keys global
let lockUploadAndDownloadModal = true
let key1 = false
let key2 = false
let optionKey = 0

document.addEventListener('keydown',(event)=>{
    if (event.keyCode == 16){
        key1 = true
    }
    if (event.keyCode == 68){
        key2 = true
        optionKey = 68
    }
    if (event.keyCode == 85){
        key2 = true
        optionKey = 85
    }

    if (key2 && key1 && optionKey == 68 && lockUploadAndDownloadModal == false){
        hideUploads()
        showDownloads()
    }
    if (key2 && key1 && optionKey == 85  && lockUploadAndDownloadModal == false){
        hideDownloads()
        showUploads()
    }
})

document.addEventListener('keyup',(event)=>{
    if (event.keyCode == 16){
        key1 = false
        optionKey = 0
    }
    if (event.keyCode == 68){
        key2 = false
        optionKey = 0
    }
})


//for document 
function fallbackCopyTextToClipboard(text) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    
    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
  
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
  
    try {
      var successful = document.execCommand('copy');
      var msg = successful ? 'successful' : 'unsuccessful';
      ShowSuccess("Copied File ID")
    } catch (err) {
      console.error('Fallback: Oops, unable to copy', err);
    }
  
    document.body.removeChild(textArea);
  }









