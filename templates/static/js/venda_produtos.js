$(document).ready(function() {
    atualizar_valor();  // Atualiza os totais ao carregar a página
});

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
                        atualizar_produto();  // Atualiza a lista de produtos
                        atualizar_valor();
                        $("#produto-autocomplete").val('');  // Limpa o campo de entrada
                    }
                }
            });
            return false;  // Previne que o valor seja inserido no campo
        }
    });

    // Função para atualizar a lista de produtos
    function atualizar_produto() {
     // Primeiro, armazena as quantidades atuais dos produtos
     var quantidadesAtuais = {};
     $('#tabela_produtos tr').each(function() {
         var produtoId = $(this).find('input[name="produto_id"]').val();
         var quantidade = $(this).find('input[name="quantidade"]').val();
         quantidadesAtuais[produtoId] = quantidade;
     });
 
     $.ajax({
         type: "GET",
         url: ProdutoSelecionadoUrl,
         success: function(response) {
             var tbody = $('#tabela_produtos');
             tbody.empty();
             response.products.forEach(function(produto) {
                 // Obtém a quantidade salva, se disponível
                 var quantidade_tela = quantidadesAtuais[produto.id] || 1;
 
                 var tr = '<tr>' +
                     '<td>' + produto.nome + '</td>' +
                     '<td>' + produto.marca + '</td>' +
                     '<td>' + produto.codigo + '</td>' +
                     '<td>R$ ' + produto.venda + '</td>' +
                     '<td>' +
                        '<input type="text" name="valor_total_peca" value="{{ valor_total_peca }}" readonly>' +
                     '</td>' +
                     '<td>' +
                         '<input type="number" name="quantidade" value="' + quantidade_tela + '" min="1">' +
                         '<input type="hidden" name="produto_id" value="' + produto.id + '">' +
                     '</td>' +
                     '<td>' +
                         '<img src="/static/img/delete.png" class="img-cancelar" data-prod-id="' + produto.id + '" alt="Cancelar" style="cursor: pointer;">' +
                     '</td>' +
                     '</tr>';
                 tbody.append(tr);
             });
             atualizar_valor();  // Atualiza o valor total após a atualização da tabela
         }
     });
 }
    $(document).on('input', 'input[name="quantidade"]', function() {
        atualizar_valor();
    });

    function atualizar_valor(){
        var valor_total_compra = 0;
        $('#tabela_produtos tr').each(function() {
            var $row = $(this);
            var valor_unidade = Number($row.find('td').eq(3).text().replace('R$', '').replace(',', '.').trim());
            var quantidade = parseInt($row.find('input[name="quantidade"]').val());
            var valor_total_peca = valor_unidade * quantidade;
            
            // Atualiza o valor total do produto na linha
            $row.find('input[name="valor_total_peca"]').val(valor_total_peca.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
            
            valor_total_compra += valor_total_peca;
        });
        
        // Atualiza o valor total de todos os produtos
        $('#valor-total').text('R$ ' + valor_total_compra.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
        $('#valor_total_compra').val(valor_total_compra)
    }

    // Lida com o clique no botão de cancelar
    $(document).on('click', '.img-cancelar', function() {
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
                    atualizar_produto();  // Atualiza a lista de produtos
                    atualizar_valor();
                }
            }
        });
    });
});
