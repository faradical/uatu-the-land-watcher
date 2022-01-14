function GET(path) {
    return new Promise(function (resolve, reject) {
        axios.get(path).then((response) => {
            resolve(response);
        }).catch((error) => {
            reject(error);
        });
    });
}

function POST(path, data) {
    return new Promise(function (resolve, reject) {
        axios.post(path, data).then((response) => {
            resolve(response);
        }).catch((error) => {
            reject(error);
        });
    });
}

d3.json("/api/cheapest_state")
    .then(function(data){
        console.log(data)
        d3.select("#state").text(data.state)
        d3.select("#price").text(data.median)
    })
    .catch(console.log("It no worky yet."))

function initMap() {
    const myLatLng = { lat: -25.363, lng: 131.044 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 4,
        center: myLatLng,
    });
  
    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "Hello World!",
    });
}





d3.select("#pac-input").on('keydown', function(e){
    if (e.code === 'Enter'){
        let search = d3.select("#pac-input").property("value")
        console.log(search)
        data = {'search': search}
        POST("/api/get_data", data).then(response => {
            console.log(response.data)
        })
    }
})
d3.select("#my_button").on('click', function(){
    let search = d3.select("#pac-input").property("value")
    console.log(search)
    data = {'search': search}
    POST("/api/get_data", data).then(response => {
        console.log(response.data)
    })

})