var offers = [];
var punto1 = "Sevilla";
var punto2 = "Lugo";

$(document).ready(function () {

    // LoadCalendar(getUrlVar("p1"), getUrlVar("p2"));
    get_offers("ida", "Sevilla", "A Coruña");
    get_offers("vuelta", "A Coruña", "Sevilla");
})

function getUrlVar(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function LoadCalendar(p1, p2) {

    get_offers("ida", p1, p2);
    get_offers("vuelta", p2, p1);
}

function get_offers(root, salida, destino) {

    $("." + root + "_month_name").each(function () {
        $(this).text($(this).text() + " " + salida + " - " + destino);
    })

    $.getJSON('./06_09_2021_' + salida + '-' + destino + '.json', function (data) { // https://acolmenero.xyz/english/words.json


        console.log("==========" + root);

        offers = data;

        prices = Object.keys(offers);
        prices.sort(function (a, b) {
            return parseInt(a) - parseInt(b);
        });
        console.log(offers[prices[0]]);



        offers[prices[0]].forEach(function (offer) {
            var horaSalida = offer.horaSalida.replaceAll(".", ":")
            var date = offer.fecha.split("_")
            var day = date[0].length == 1 ? "0" + date[0] : date[0];
            var month = date[1].length == 1 ? "0" + date[1] : date[1];

            var day_div = $("#" + root + "" + day + "-" + month)
            day_div.html(day_div.html() + "<div class='offer'><a href=" + offer.url + ">" + offer.type + " " + horaSalida + ": <strong>" + prices[0] + "€</strong><a></div>")

        })
        if (prices.length != 1) {
            offers[prices[1]].forEach(function (offer) {
                var horaSalida = offer.horaSalida.replaceAll(".", ":")
                var date = offer.fecha.split("_")
                var day = date[0].length == 1 ? "0" + date[0] : date[0];
                var month = date[1].length == 1 ? "0" + date[1] : date[1];

                var day_div = $("#" + root + "" + day + "-" + month);
                day_div.html(day_div.html() + "<div class='offer'><a href=" + offer.url + ">" + offer.type + " " + horaSalida + ": <strong>" + prices[1] + "€</strong><a></div>")

            })
        } 
        // if (prices.length != 2) {
        //     offers[prices[2]].forEach(function (offer) {
        //         var horaSalida = offer.horaSalida.replaceAll(".", ":")
        //         var date = offer.fecha.split("_")
        //         var day = date[0].length == 1 ? "0" + date[0] : date[0];
        //         var month = date[1].length == 1 ? "0" + date[1] : date[1];

        //         var day_div = $("#" + root + "" + day + "-" + month)
        //         day_div.html(day_div.html() + "<div class='offer'><a href=" + offer.url + ">" + offer.type + " " + horaSalida + ": <strong>" + prices[2] + "€</strong><a></div>")

        //     })
        // }

        console.log(prices[0]);
        console.log(prices[1]);
        console.log(prices[2]);

    });

}


// https://www.alsa.es/checkout?p_p_id=PurchasePortlet_WAR_Alsaportlet&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_PurchasePortlet_WAR_Alsaportlet_javax.portlet.action=searchJourneysAction&p_auth=YFT0JB8j&code=&serviceType=&accessible=0&originStationNameId=A%20Coru%C3%B1a%2F%20La%20Coru%C3%B1a&originStationId=377&destinationStationNameId=Sevilla%20(Todas%20las%20paradas)&destinationStationId=90340&departureDate=08%2F09%2F2021&locationMode=&passengerType-1=1&passengerType-4=0&passengerType-5=0&passengerType-2=0&passengerType-3=0&numPassengers=1&regionalZone=&travelType=OUTWARD&LIFERAY_SHARED_isTrainTrip=false&promoCode=&jsonAlsaPassPassenger=&jsonVoucherPassenger=