$(function() {
    // Configura o autocomplete para o campo de entrada com ID "produto-autocomplete"
    $("#produto-autocomplete").autocomplete({
        source: lista_de_produtos,  // Define a lista de produtos disponíveis para autocomplete
        select: function(event, ui) {  // Função executada quando um item é selecionado
            $.ajax({
                type: "POST",  // Tipo de requisição HTTP
                url: addProdutoUrl,  // URL para onde a requisição será enviada
                data: {  // Dados enviados na requisição
                    produto_id: ui.item.value,  // ID do produto selecionado
                    csrfmiddlewaretoken: csrfToken  // Token CSRF para segurança
                },
                success: function(response) {  // Função executada em caso de sucesso na requisição
                    if (response.status === 'success') {  // Verifica se a resposta indica sucesso
                        updateListProdutos();  // Atualiza a lista de produtos
                        $("#produto-autocomplete").val('');  // Limpa o campo de entrada
                    }
                }
            });
            return false;  // Previne que o valor seja inserido no campo
        }
    });

    // Função para atualizar a lista de produtos
    function updateListProdutos() {
        $.ajax({
            type: "GET",  // Tipo de requisição HTTP
            url: ProdutoSelecionadoUrl,  // URL para onde a requisição será enviada
            success: function(response) {  // Função executada em caso de sucesso na requisição
                var tbody = $('#tabela_produtos');  // Seleciona o elemento tbody da tabela de produtos
                tbody.empty();  // Limpa o conteúdo atual do tbody
                response.products.forEach(function(produto) {  // Itera sobre cada produto na resposta
                    var tr = '<tr>' +
                        '<td>' + produto.nome + '</td>' +  // Nome do produto
                        '<td>' + produto.marca + '</td>' +  // Marca do produto
                        '<td>' + produto.codigo + '</td>' +  // Código do produto
                        '<td>R$ ' + produto.venda + '</td>' +  // Preço de venda do produto
                        '<td>1</td>' +  // Quantidade (ajustar conforme necessário)
                        '<td><button class="btn-cancelar" data-prod-id="' + produto.id + '">Cancelar</button></td>' +  // Botão de cancelar
                        '</tr>';
                    tbody.append(tr);  // Adiciona a linha na tabela
                });
            }
        });
    }

    // Lida com o clique no botão de cancelar
    $(document).on('click', '.btn-cancelar', function() {
        var prodId = $(this).data('prod-id');  // Obtém o ID do produto a ser removido
        $.ajax({
            type: "POST",  // Tipo de requisição HTTP
            url: removeProductUrl,  // URL para onde a requisição será enviada
            data: {  // Dados enviados na requisição
                produto_id: prodId,  // ID do produto a ser removido
                csrfmiddlewaretoken: csrfToken  // Token CSRF para segurança
            },
            success: function(response) {  // Função executada em caso de sucesso na requisição
                if (response.status === 'success') {  // Verifica se a resposta indica sucesso
                    updateListProdutos();  // Atualiza a lista de produtos
                }
            }
        });
    });
});
