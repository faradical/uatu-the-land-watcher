d3.json("http://127.0.0.1:5000/cheapest_state")
    .then(function(data){
        console.log(data)
        d3.select("#state").text(data.state)
        d3.select("#price").text(data.median)
    })
    .catch(console.log("It no work."))
