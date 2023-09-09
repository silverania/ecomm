var text = "";
var trunc = "";
$(document).ready(function () {
    objectproducts = new Array();
    function cleanJson(json) {
        var data = json.toString();
        s = data
            .replace(/\\n/g, "\\n")
            .replace(/\\'/g, "\\'")
            .replace(/\\"/g, '\\"')
            .replace(/\\&/g, "\\&")
            .replace(/\\r/g, "\\r")
            .replace(/\\t/g, "\\t")
            .replace(/\\b/g, "\\b")
            .replace(/\\f/g, "\\f")
            .replace("&quot;", "");
        return s;
    }
    //products = cleanJson(products);
    category = cleanJson(category);
    var i = 0;
    var elulproduct = document.querySelector('#ulproduct');
    while (i < products.length) {
        objectproducts.push(products[i].fields.name);
        var hreflink = "href=" + BASE_URL + category + "/" + products[i].fields.slug
        var id_li = " id=\"li_product_" + products[i].fields.name + "\"";
        $(elulproduct).append('<li' + id_li + '><a ' + hreflink + ">" + products[i].fields.name.substring('0', '30') + ".." + '</a ></li > ');
        i++;
    }
    //category = JSON.parse(category);
    /*var impl = document.implementation,
        xmlDoc = impl.createDocument(namespaceURI, qualifiedNameStr, documentType),
        htmlDoc = impl.createHTMLDocument(title);*/
    class Product {
        constructor(
            manager = "anonimo",
            products = "",
            prodname = "",
            slug = "",
            description = "",
            price = 0,
            rootlink = "",

        ) {
            this.manager = manager;
            this.products = products;
            this.prodname = prodname;
            this.slug = slug;
            this.description = description;
            //this.titled=title1
            this.slug = slug;
            this.price = price;
            this.rootlink = rootlink;
        }
    }
    /* tronco il testo in descrizione */
    text = document.getElementById("truncate").innerHTML;
    var truncated = text.substring(0, 300);
    document.getElementById("truncate").innerHTML = truncated + '<span id="s_continua"> continua....</span>';
    trunc = true;
});

function truncateText() {
    if (trunc === true || trunc === undefined) {
        document.getElementById("truncate").innerHTML = text;
        trunc = false;
    }
    else {
        var truncated = text.substring(0, 300) + "...continua";
        document.getElementById("truncate").innerHTML = truncated;
        trunc = true;
    }
}
