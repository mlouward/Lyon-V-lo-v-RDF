const listStations = document.getElementById("list-stations")
const searchbar = document.getElementById("searchbar")

searchbar.addEventListener('input', _ => {
  // Search with regex (case-insensititve and anywhere in the name/adddress of bike station)
  const searchTerms = escapeRegExp(searchbar.value);
  let searchResults = window.stations;
  if (searchTerms !== "") {
    const exp = new RegExp(searchTerms, 'ig');
    // filter regex matches on address or name of station
    searchResults = window.stations.filter((x) => {
      if (x.name.search(exp) > -1 || x.address.search(exp) > -1)
        return x;
    })
  }

  // remove all cards
  while (listStations.firstChild) {
    listStations.firstChild.remove()
  }
  // sort results
  searchResults.sort((a, b) => (a.name > b.name) ? 1 : -1)
  // add the matching cards
  addCards(searchResults);
})


function displayBikestands(stations) {
  // Don't display stations with no name
  window.stations = stations.filter((x) => { return x.name !== '' })
  // Sort by alphabetical order
  window.stations.sort((a, b) => (a.name > b.name) ? 1 : -1)

  // iterate over all of our stations and create a card for each of them
  // with required info
  addCards(window.stations)
}

function addCards(stations) {
  for (const s of stations) {
    // Create card element and add requiered info
    const card = document.createElement('div')
    card.classList = 'card';

    const stationName = document.createElement('h2')
    stationName.innerHTML = `${s.name}`
    card.appendChild(stationName)

    const stationAddress = document.createElement('p')
    stationAddress.innerHTML = `${s.address}`
    card.appendChild(stationAddress)

    const bikeWrapper = document.createElement('div')
    bikeWrapper.classList = 'bike-wrapper'
    card.appendChild(bikeWrapper)

    const availableBikes = document.createElement('p')
    availableBikes.innerHTML = `Vélos disponibles: ${s.available_bikes}`
    bikeWrapper.appendChild(availableBikes)

    const availableBikeStands = document.createElement('p')
    availableBikeStands.innerHTML = `Places disponibles: ${s.available_bike_stands}`
    availableBikeStands.style = 'margin-left: auto'
    bikeWrapper.appendChild(availableBikeStands)

    const lastUpdate = document.createElement('p')
    lastUpdate.style = 'text-align: right; color: #666'
    lastUpdate.innerHTML = `Last update: ${s.last_update}`
    card.appendChild(lastUpdate)

    // Add element to our list
    listStations.appendChild(card)
  }
}

function escapeRegExp(s) {
  return s.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')
}