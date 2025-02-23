
wilayaCombobox = document.getElementById('wilayaId')
dayraCombobox = document.getElementById('dayraId')
municipalityCombobox = document.getElementById('municipalityId')

wilayaList = [];
for (var index=0 ; index<wilayaCombobox.length; index++){
    id = wilayaCombobox.options[index].value;
    name_ = wilayaCombobox.options[index].text;;
    wilayaList.push({id: id, name_: name_});
}

dayraList = [];
for (var index=0 ; index<dayraCombobox.length; index++){
    id = dayraCombobox.options[index].value;
    name_ = dayraCombobox.options[index].text;
    wilayaId = dayraCombobox.options[index].getAttribute("class");
    dayraList.push({id: id, name_: name_, wilayaId: wilayaId});
}

municipalityList = [];
for (var index=0 ; index<municipalityCombobox.length; index++){
    id = municipalityCombobox.options[index].value;
    name_ = municipalityCombobox.options[index].text;
    dayraId = municipalityCombobox.options[index].getAttribute("class");
    municipalityList.push({id: id, name_: name_, dayraId: dayraId});
}



function updateWilayaSelectField(){
    wilayaCombobox.innerHTML = "";

    const option = document.createElement("option");
    option.value = 0;
    option.textContent = "الولاية";
    wilayaCombobox.appendChild(option);
    for (var i=0 ; i<wilayaList.length; i++){
        const option = document.createElement("option");
        option.value = wilayaList[i].id;
        option.textContent = wilayaList[i].name_;
        wilayaCombobox.appendChild(option);
    }
    wilayaCombobox.options[0].disabled = true;
}

function updateDayraSelectField(){
    const wilaya = wilayaCombobox.options[wilayaCombobox.selectedIndex].value;
    
    dayraCombobox.innerHTML = "";

    const option = document.createElement("option");
    option.value = 0;
    option.textContent = "الدائرة";
    dayraCombobox.appendChild(option);
    for (var i=0 ; i<dayraList.length; i++){
        if (dayraList[i].wilayaId == wilaya){
            const option = document.createElement("option");
            option.value = dayraList[i].id;
            option.textContent = dayraList[i].name_;
            dayraCombobox.appendChild(option);
        }
    }
    dayraCombobox.options[0].disabled = true;
    updateMunicipalitySelectField();
}


function updateMunicipalitySelectField(){
    const dayra = dayraCombobox.options[dayraCombobox.selectedIndex].value;
    
    municipalityCombobox.innerHTML = "";

    const option = document.createElement("option");
    option.value = 0;
    option.textContent = "البلدية";
    municipalityCombobox.appendChild(option);
    for (var i=0 ; i<municipalityList.length; i++){
        if (municipalityList[i].dayraId == dayra){
            const option = document.createElement("option");
            option.value = municipalityList[i].id;
            option.textContent = municipalityList[i].name_;
            municipalityCombobox.appendChild(option);
        }
    }
    municipalityCombobox.options[0].disabled = true;
}


wilayaCombobox.addEventListener("change", updateDayraSelectField);
dayraCombobox.addEventListener("change", updateMunicipalitySelectField);

updateWilayaSelectField();
updateDayraSelectField();
updateMunicipalitySelectField();