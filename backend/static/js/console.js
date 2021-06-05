//Variables
let imagesToCache =['background00.png', 'icons8-account-96.png', 'icons8-android-os-52.png', 'icons8-bell-48.png', 'icons8-bell-96.png', 'icons8-blind-60.png', 'icons8-chevron-right-48.png', 'icons8-cloud-96.png', 'icons8-cloud-connection-256.png', 'icons8-cloudshot.svg', 'icons8-credit-card-48.png', 'icons8-doughnut-chart-96.png', 'icons8-download-graph-report-96.png', 'icons8-empty-trash-60.png', 'icons8-folder (1).svg', 'icons8-folder-96.png', 'icons8-folder.svg', 'icons8-full-trash-100.png', 'icons8-home-96.png', 'icons8-key-128.png', 'icons8-landlord-96.png', 'icons8-microsoft-admin-90.png', 'icons8-pdf-96.png', 'icons8-right-48.png', 'icons8-search.svg', 'icons8-settings-52.png', 'icons8-settings-96.png', 'icons8-settings.svg', 'icons8-share.svg', 'icons8-sign-mail-96 (1).png', 'icons8-sign-mail-96.png', 'icons8-team-48.png', 'icons8-user-male.svg', 'icons8-video-96.png', 'icons8-windows-client-48.png'] ;

//Start
window.addEventListener('DOMContentLoaded', function() {

    //start preloading images
    for (var i=0;i != imagesToCache.length; i++){
        imagesToCache[i] = window.location.origin + "/static/console/"+imagesToCache[i]
    }
    preloadImages(imagesToCache)
    //disable loading
    //document.getElementById("loadingModal").style.display = "none"
    
    
    //should happen after all images have loaded
    setTimeout(() => {
        Promise.all(Array.from(document.images).filter(img => !img.complete).map(img => new Promise(resolve => { img.onload = img.onerror = resolve; }))).then(() => {
            var loadingModal = document.getElementById("loadingModal")
            //complete loading
            var bar = document.getElementById("loadingBar")
            bar.classList.add("finish")
            setTimeout(function(){
                loadingModal.style.display = "none"
            },1100)     
        });
    }, 3500) 
})


//
//document
function disableScrolling() {
    var x = window.scrollX;
    var y = window.scrollY;
    window.onscroll = function() { window.scrollTo(x, y); };
}

// Cache
function preloadImages(array) {
    if (!preloadImages.list) {
        preloadImages.list = [];
    }
    var list = preloadImages.list;
    for (var i = 0; i < array.length; i++) {
        var img = new Image();
        img.onload = function() {
            var index = list.indexOf(this);
            if (index !== -1) {
                // remove image from the array once it's loaded
                // for memory consumption reasons
                list.splice(index, 1);
            }
        }
        list.push(img);
        img.src = array[i];
    }
}






