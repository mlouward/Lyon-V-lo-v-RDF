const listStations = document.getElementById("list-stations")

function displayBikestands(stations) {
  // iterate over all of our stations and create a card for each of them
  // with required info
  for (const s of stations) {
    // Create card element and add requiered info
    document.createElement('li')
    // Add element to our list
    listStations.appendChild(station)
  }
}
