    //demonstration modal to act on
    let demonstrationModal = null
    let demonstationModalSlideCount = 0
    let demonstationModalCurrentPosition = 1 

    // Demonstration Object Class
    let DemonstrationObject = class {
        //constructor
        constructor(videoURL,description,body){
            this.videoURL =  videoURL
            this.description =  description
            this.body =  body
        }

    }

    //List to show objects
    let DemonstrationModalObjects = []


    //initialize 
    function initializeDemonstrationModal(element_id){
        demonstrationModal = document.getElementById(element_id)

    }

    //function 
    // Sets the modal visible to the client
    function demonstationModalSetShow(show){
        if (demonstrationModal != null){
            if (show){
                if (!demonstrationModal.classList.contains("show")){
                    demonstrationModal.classList.add("show")
                }
                return
            }
            demonstrationModal.classList.remove("show")
        }
    }

    //loads demonstration modal
    function loadDemonstrationModal(objects){
        //add elements to array
        DemonstrationModalObjects = objects

        //preload video 2 to n
        video_url_list = []

        objects.forEach(object => {
           video_url_list.push(object.videoURL)
        });

        preloadVideos(video_url_list)

        

        //set slide count
        demonstationModalSlideCount = DemonstrationModalObjects.length

        //reset slide count
        demonstationModalCurrentPosition = 1
        
        //set description
        demonstrationModalShowSlide(demonstationModalCurrentPosition)

        //show 
        demonstationModalSetShow(true)
    }

    //show slide
    // will handle switching of slides 
    function demonstrationModalShowSlide(number){
        //index starts at zero 
        var indexed_number = number - 1

        setDemonstrationModalSlideNumber(number)
        setDemonstrationModalVideoUrl(DemonstrationModalObjects[indexed_number].videoURL)
        setDemonstrationModalDescription(DemonstrationModalObjects[indexed_number].description)
        setDemonstrationModalBody(DemonstrationModalObjects[indexed_number].body)
    }

    //next , show the next slide
    function demonstationModalSlideNext(){
        //check if not end of object list
        if (demonstationModalCurrentPosition < DemonstrationModalObjects.length){
            demonstationModalCurrentPosition ++
        }
        
        demonstrationModalShowSlide(demonstationModalCurrentPosition)
    }

    //next , show the next slide
    function demonstationModalSlidePrevious(){
        //check if not end of object list
        if (demonstationModalCurrentPosition > 1){
            demonstationModalCurrentPosition --
        }
        
        demonstrationModalShowSlide(demonstationModalCurrentPosition)
    }

    //set description
    function setDemonstrationModalDescription(description){
        var descriptionElement = GetElementInsideContainer(demonstrationModal,"description")
        descriptionElement.innerText = description 
    }

    //set body 
    function setDemonstrationModalBody(body){
        var bodyElement = GetElementInsideContainer(demonstrationModal,"demonstrationBody")
        bodyElement.innerText = body
    }

    //set slide
    function setDemonstrationModalSlideNumber(number){
        var slideNumberElement = GetElementInsideContainer(demonstrationModal,"slideNumber")
        //set video 

        slideNumberElement.innerText = `Slide ${number}/${DemonstrationModalObjects.length}`
    }
    
    //set video current video url
    function setDemonstrationModalVideoUrl(url){
        var videoPlayer = GetElementInsideContainer(demonstrationModal,"videoPlayer")
        videoPlayer.src = url
    }

    // get element inside div
    function GetElementInsideContainer(container, childID) {
    var elm = {};
    var elms = container.getElementsByTagName("*");
        for (var i = 0; i < elms.length; i++) {
            if (elms[i].id === childID) {
                elm = elms[i];
                break;
            }
        }
        return elm;
    }

    function preloadVideos(array) {
        if (!preloadVideos.list) {
            preloadVideos.list = [];
        }
        var list = preloadVideos.list;
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
