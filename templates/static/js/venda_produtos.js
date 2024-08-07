$(function() {
    $("#produto-autocomplete").autocomplete({
        source: availableProducts,
        select: function(event, ui) {
            $.ajax({
                type: "POST",
                url: addProductUrl,
                data: {
                    product_id: ui.item.value,
                    csrfmiddlewaretoken: csrfToken
                },
                success: function(response) {
                    if (response.status === 'success') {
                        updateProductList();
                        $("#produto-autocomplete").val(''); // Limpa o campo de entrada
                    }
                }
            });
            return false; // Previne que o valor seja inserido no campo
        }
    });

    function updateProductList() {
        $.ajax({
            type: "GET",
            url: getSelectedProductsUrl,
            success: function(response) {
                var tbody = $('#selected-products');
                tbody.empty();
                response.products.forEach(function(produto) {
                    var tr = '<tr>' +
                        '<td>' + produto.nome + '</td>' +
                        '<td>' + produto.marca + '</td>' +
                        '<td>' + produto.codigo + '</td>' +
                        '<td>R$ ' + produto.venda + '</td>' +
                        '<td>1</td>' + 
                        '<td><button class="btn-cancelar" data-prod-id="' + produto.id + '">Cancelar</button></td>' +
                        '</tr>';
                    tbody.append(tr);
                });
            }
        });
    }

    // Handle cancel button click
    $(document).on('click', '.btn-cancelar', function() {
        var prodId = $(this).data('prod-id');
        $.ajax({
            type: "POST",
            url: removeProductUrl,
            data: {
                product_id: prodId,
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.status === 'success') {
                    updateProductList();
                }
            }
        });
    });
});
