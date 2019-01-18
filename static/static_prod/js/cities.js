"use strict";
let data = {};
let countriesByAbbreviation = [{
  country: "",
  abbreviation: null
}];
  data.town = 'test';
  url = "{% url 'cities_streets' %}";
  $.ajax({
      url: url,
      type: 'POST',
      data: data,
      dataType: "json",
      cache: true,
      headers: {'X-CSRFToken': '{{ csrf_token }}'},
      success: function (data) {
            $.each(data.cities, function (k, v) {
               countriesByAbbreviation['country'] = v.name_of_city;
               countriesByAbbreviation['abbreviation'] = null
            })
          },
      error: function () {
          console.log("error read 'cities'")
      },
      });


let filterCountriesOnChange = function filterCountriesOnChange(event) {
  let value = event.target.value.toLowerCase();

  let result = countriesByAbbreviation.filter(function (countryObject) {
    let abbreviation = countryObject.abbreviation || '';
    let country = countryObject.country || '';
    let countryString = abbreviation + " " + country;

    return countryString.toLowerCase().includes(value);
  });

  generateCountriesList(result);
};

let addEventListenerToCountries = function addEventListenerToCountries() {
  let countriesInput = document.querySelector('.countries-input');
  let countryListItems = document.querySelectorAll('.country');
  let countryListItemIndex = 0;
  let countryListItemILength = countryListItems.length;

  for (countryListItemIndex; countryListItemIndex < countryListItemILength; countryListItemIndex++) {
    let countryListItem = countryListItems[countryListItemIndex];

    countryListItem.addEventListener('mousedown', function (event) {
      event.preventDefault();
      event.stopPropagation();

      let value = event.currentTarget.innerText;
      countriesInput.value = value;

      filterCountriesOnChange({ target: { value: value } });

      countriesInput.focus();
    });
  }
};

let createCountryListItem = function createCountryListItem(_ref) {
  let _ref$country = _ref.country,
      country = _ref$country === undefined ? '' : _ref$country,
      _ref$abbreviation = _ref.abbreviation,
      abbreviation = _ref$abbreviation === undefined ? '' : _ref$abbreviation;
  return "<li class=\"country\" data-value=\"" + abbreviation + " " + country + "\"><span class=\"country--abbreviation\">" + abbreviation + "</span> <span class=\"country--name\">" + country + "</span></li>";
};

let generateCountriesList = function generateCountriesList(countriesArray) {
  let countriesList = document.querySelector('.countries-list');
  countriesList.innerHTML = '';

  let countriesLength = countriesArray.length;

  for (let countryIndex = 0; countryIndex < countriesLength; countryIndex++) {
    countriesList.innerHTML += createCountryListItem(countriesArray[countryIndex]);
  }

  addEventListenerToCountries();
};

document.addEventListener("DOMContentLoaded", function () {
  let countriesInput = document.querySelector('.countries-input');

  generateCountriesList(countriesByAbbreviation);

  countriesInput.addEventListener('keyup', filterCountriesOnChange);

  countriesInput.addEventListener('focus', function () {
    let countriesList = document.querySelector('.countries-list-container');
    countriesList.classList.add('visible');
  });

  countriesInput.addEventListener('blur', function (event) {
    let countriesList = document.querySelector('.countries-list-container');
    countriesList.classList.remove('visible');
  });
});