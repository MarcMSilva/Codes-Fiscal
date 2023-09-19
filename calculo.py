import PySimpleGUI as sg
import pandas as pd
import os


font = ('Arial', 8)

# Limpar o resultado/valor líquido
def limparConsulta():
      janela['codImp1'] .update('')
      janela['base1'] .update('')
      janela['valor1'] .update('')
      janela['codImp2'] .update('')
      janela['base2'] .update('')
      janela['valor2'] .update('')
      janela['codImp3'] .update('')
      janela['base3'] .update('')
      janela['valor3'] .update('')
      janela['codImp4'] .update('')
      janela['base4'] .update('')
      janela['valor4'] .update('')
      janela['valorLiquido'] .update('')

#Layout
def janelaInicial():
      sg.theme('Dark Brown 1')
      layout = [
            [sg.Text(''), sg.Text(''), sg.Text(''), sg.Text(''), sg.Text(''), sg.Text('Valor da Nota Fiscal:')],
            [sg.Text(''), sg.Text(''), sg.Text(''), sg.Text(''), sg.Text(''), sg.Text('R$'), sg.InputText(key='valorNotaFiscal', size=(10))],
            [sg.Text('')],
            [sg.Text('IS:', size=(4)), sg.InputText('5.00', key='aliqISS', size=(4)), sg.Text('%'), sg.Text('', size=(4)), sg.Text('Dedução:'), sg.InputText('0', key='dedValor', size=(6))],
            [sg.Text('INSS:'), sg.Button('11%', key='inss11'), sg.Button('3.5%', key='inss35'), sg.Text(''), sg.Text('Base:'), sg.InputText('100', key='inssDed', size=(4)), sg.Text('%')],
            [sg.Text('IR:', size=(4)), sg.Button('1.5%', key='ir15'), sg.Button('1.0%', key='ir10')],
            [sg.Text('')],
            [sg.Button('PCC/IR'), sg.Button('PCC/IR/IS', size=(9)), sg.Button('PCC/IS'), sg.Button('PCC', size=(6))],
            [sg.Button('IS', size=(5)), sg.Button('PCC/IN/IR/IS'), sg.Button('IR/IS', size=(6)), sg.Button('ERAM', size=(5))],
            [sg.Button('INSS', size=(5)), sg.Button('PCC/IN/IR', size=(10)), sg.Button('IN/IS', size=(5)), sg.Button('IR', size=(6))],
            [sg.Text(''), sg.Text(''), sg.InputText(key='codImp1', size=(5)), sg.InputText(key='base1', size=(10)), sg.InputText(key='valor1', size=(10))],
            [sg.Text(''), sg.Text(''), sg.InputText(key='codImp2', size=(5)), sg.InputText(key='base2', size=(10)), sg.InputText(key='valor2', size=(10))],
            [sg.Text(''), sg.Text(''), sg.InputText(key='codImp3', size=(5)), sg.InputText(key='base3', size=(10)), sg.InputText(key='valor3', size=(10))],
            [sg.Text(''), sg.Text(''), sg.InputText(key='codImp4', size=(5)), sg.InputText(key='base4', size=(10)), sg.InputText(key='valor4', size=(10))],
            [sg.Text(''), sg.Text(''), sg.Text(key='valorLiquido')],
            [sg.Text('', size=(10,0)), sg.Button('Copiar Valores')],
            [sg.Text('')],
            [sg.Text('', size=(6,0)), sg.Text('Criado por Marcelo MSilva. v1.1!', font=font)],

      ]
      return sg.Window('Calculadora de impostos retidos na fonte v1.0', layout, finalize=True)

#Criar janelas inicias
janela = janelaInicial()


#Declarando variáveis
IR = (1.5 / 100)
IS = (5 / 100)
IN = (11 / 100)
INDed = 100
ISDed = 0


#Lendo ações
while True:
      evento, valores = janela.read()

      # Se o evento for clicar no botão de fechar, então encerrar o programa.
      if evento == sg.WIN_CLOSED:
            break


      # Se o valor de valorNotaFiscal for nulo, então continue no looping
      if valores['valorNotaFiscal'] == '':
            continue


      # Define o valor inserido no campo valorNotaFiscal como float
      try:
            fValorNF = float(valores['valorNotaFiscal'])
      except ValueError:
            sg.popup('Verificar o valor da nota fiscal.')
            continue


      # Se o valor de dedValor for nulo, então será 0
      if valores['dedValor'] == '':
            valores['dedValor'] = 0


      # Transforma o valor inserido no input dedValor em varíavel e float
      valorISDed = valores['dedValor']
      try:
            ISDed = float(valorISDed)
      except ValueError:
            sg.popup('Verificar o valor da dedução do ISSQN.')
            continue
      ISDed = float(valorISDed)


      # Se o valor de aliqISS for nulo, então será 0
      if valores['aliqISS'] == '':
            valores['aliqISS'] = 0


      # Transforma o valor inserido no input ISS em varíavel e float
      valorIS = valores['aliqISS']
      try:
            IS = float(valorIS)
      except ValueError:
            sg.popup('Verificar da alíquota do ISSQN.')
            continue
      IS = float(valorIS)
      ISReturn = IS


      # Se clicar no botão de 11% a váriavel IN será setada a 11%
      if evento == 'inss11':
            IN = (11 / 100)


      # Se clicar no botão de 3.5% a váriavel IN será setada a 3.5%
      if evento == 'inss35':
            IN = (3.5 / 100)


      # Transforma o valor inserido no input INDed em varíavel e float
      valorDed = valores['inssDed']


      #Se não tiver valor na base do INSS, o valor será 0
      if valorDed == '':
            valorDed = 0


      #Se o valor da base do INSS for colocado com vírgula, irá gerar o seguinte erro:
      try:
            INDed = float(valorDed)
      except ValueError:
            sg.popup('Verificar da base do INSS.')
            continue
      INDed = float(valorDed)
      INReturn = IN


      # Se clicar no botão de 1.0% a váriavel IR será setada a 1.0%
      if evento == 'ir10':
            IR = (1 / 100)


      # Se clicar no botão de 1.5% a váriavel IR será setada a 1.5%
      if evento == 'ir15':
            IR = (1.5 / 100)


      #Declara o valor de IRReturn para o valor do IR
      IRReturn = IR



      # Se clicar no botão PCC/IR então:
      if evento == 'PCC/IR':
            limparConsulta()
            PCC = fValorNF * (4.65 / 100)
            IR = fValorNF * (IR)

            valorLiq = fValorNF - PCC - IR
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertPCC = f'{PCC:_.2f}'
            PCC = convertPCC.replace('.', ',').replace('_', '.')

            convertIR = f'{IR:_.2f}'
            IR = convertIR.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            basePCC = valorNF

            baseIR = valorNF

            janela['codImp1'] .update('PCC:')
            janela['base1'] .update(basePCC)
            janela['valor1'] .update(PCC)
            janela['codImp2'] .update('IR:')
            janela['base2'] .update(baseIR)
            janela['valor2'] .update(IR)
            janela['valorLiquido'] .update(f'O valor líquido é: {valorLiq}')

            IR = IRReturn



      # Se o evento for clicar no botão PCC/IR/IS, então:
      if evento == 'PCC/IR/IS':
            limparConsulta()
            PCC = fValorNF * (4.65 / 100)
            IR = fValorNF * (IR)
            IS = (fValorNF - ISDed ) * IS / 100

            valorLiq = fValorNF - PCC - IR - IS
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertPCC = f'{PCC:_.2f}'
            PCC = convertPCC.replace('.', ',').replace('_', '.')

            convertIR = f'{IR:_.2f}'
            IR = convertIR.replace('.', ',').replace('_', '.')

            convertIS = f'{IS:_.2f}'
            IS = convertIS.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            basePCC = valorNF

            baseIR = valorNF

            baseIS = fValorNF - ISDed
            convertBaseIS = f'{baseIS:_.2f}'
            baseIS = convertBaseIS.replace('.', ',').replace('_', '.')

            janela['codImp1'] .update('PCC:')
            janela['base1'] .update(basePCC)
            janela['valor1'] .update(PCC)
            janela['codImp2'] .update('IR:')
            janela['base2'] .update(baseIR)
            janela['valor2'] .update(IR)
            janela['codImp3'] .update('IS:')
            janela['base3'] .update(baseIS)
            janela['valor3'] .update(IS)
            janela['valorLiquido'] .update(f'O valor líquido é: {valorLiq}')

            IR = IRReturn
            IS = ISReturn



      # Se o evento for clicar no botão PCC/IS, então:
      if evento == 'PCC/IS':
            limparConsulta()
            PCC = fValorNF * (4.65 / 100)
            IS = (fValorNF - ISDed) * IS / 100

            valorLiq = fValorNF - PCC - IS
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertPCC = f'{PCC:_.2f}'
            PCC = convertPCC.replace('.', ',').replace('_', '.')

            convertIS = f'{IS:_.2f}'
            IS = convertIS.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            basePCC = valorNF

            baseIS = fValorNF - ISDed
            convertBaseIS = f'{baseIS:_.2f}'
            baseIS = convertBaseIS.replace('.', ',').replace('_', '.')

            janela['codImp1'] .update('PCC:')
            janela['base1'] .update(basePCC)
            janela['valor1'] .update(PCC)
            janela['codImp2'] .update('IS:')
            janela['base2'] .update(baseIS)
            janela['valor2'] .update(IS)
            janela['valorLiquido'] .update(f'O valor líquido é: {valorLiq}')

            IS = ISReturn



      # Se o evento for clicar no botão PCC, então:
      if evento == 'PCC':
            limparConsulta()
            PCC = fValorNF * (4.65 / 100)

            valorLiq = fValorNF - PCC
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertPCC = f'{PCC:_.2f}'
            PCC = convertPCC.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            basePCC = valorNF

            janela['codImp1'].update('PCC:')
            janela['base1'].update(basePCC)
            janela['valor1'].update(PCC)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')



      # Se o evento for clicar no botão IS, então:
      if evento == 'IS':
            limparConsulta()
            IS = (fValorNF - ISDed) * IS / 100

            valorLiq = fValorNF - IS
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertIS = f'{IS:_.2f}'
            IS = convertIS.replace('.', ',').replace('_', '.')

            baseIS = fValorNF - ISDed
            convertBaseIS = f'{baseIS:_.2f}'
            baseIS = convertBaseIS.replace('.', ',').replace('_', '.')

            janela['codImp1'].update('IS:')
            janela['base1'].update(baseIS)
            janela['valor1'].update(IS)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')

            IS = ISReturn



      # Se o evento for clicar no botão PCC/IN/IR/IS, então:
      if evento == 'PCC/IN/IR/IS':
            limparConsulta()
            PCC = fValorNF * (4.65 / 100)
            IN = (fValorNF * (INDed / 100)) * IN
            IR = fValorNF * (IR)
            IS = (fValorNF - ISDed) * IS / 100

            valorLiq = fValorNF - PCC - IN - IR - IS
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertPCC = f'{PCC:_.2f}'
            PCC = convertPCC.replace('.', ',').replace('_', '.')

            convertIN = f'{IN:_.2f}'
            IN = convertIN.replace('.', ',').replace('_', '.')

            convertIR = f'{IR:_.2f}'
            IR = convertIR.replace('.', ',').replace('_', '.')

            convertIS = f'{IS:_.2f}'
            IS = convertIS.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            basePCC = valorNF

            baseIN = fValorNF * (INDed / 100)
            convertBaseIN = f'{baseIN:_.2f}'
            baseIN = convertBaseIN.replace('.', ',').replace('_', '.')

            baseIR = valorNF

            baseIS = fValorNF - ISDed
            convertBaseIS = f'{baseIS:_.2f}'
            baseIS = convertBaseIS.replace('.', ',').replace('_', '.')

            janela['codImp1'].update('PCC:')
            janela['base1'].update(basePCC)
            janela['valor1'].update(PCC)
            janela['codImp2'].update('IN:')
            janela['base2'].update(baseIN)
            janela['valor2'].update(IN)
            janela['codImp3'].update('IR:')
            janela['base3'].update(baseIR)
            janela['valor3'].update(IR)
            janela['codImp4'].update('IS:')
            janela['base4'].update(baseIS)
            janela['valor4'].update(IS)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')

            IR = IRReturn
            IS = ISReturn
            IN = INReturn



      # Se o evento for clicar no botão IR/IS, então:
      if evento == 'IR/IS':
            limparConsulta()
            IR = fValorNF * (IR)
            IS = (fValorNF - ISDed) * IS / 100

            valorLiq = fValorNF - IR - IS
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            convertIR = f'{IR:_.2f}'
            IR = convertIR.replace('.', ',').replace('_', '.')

            convertIS = f'{IS:_.2f}'
            IS = convertIS.replace('.', ',').replace('_', '.')

            baseIR = valorNF

            convertBaseIS = fValorNF - ISDed
            baseIS = f'{convertBaseIS:_.2f}'
            baseIS = baseIS.replace('.', ',').replace('_', '.')

            janela['codImp1'].update('IR:')
            janela['base1'].update(baseIR)
            janela['valor1'].update(IR)
            janela['codImp2'].update('IS:')
            janela['base2'].update(baseIS)
            janela['valor2'].update(IS)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')

            IR = IRReturn
            IS = ISReturn

      # Se o evento for clicar no botão ERAM, então:
      if evento == 'ERAM':
            limparConsulta()
            CS = fValorNF * (1 / 100)
            IN = fValorNF * (50 / 100) * (3.5 / 100)
            IR = fValorNF * (1.5 / 100)
            IS = fValorNF * (50 / 100) * (5 / 100)

            valorLiq = fValorNF - CS - IN - IR - IS
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            convertCS = f'{CS:_.2f}'
            CS = convertCS.replace('.', ',').replace('_', '.')

            convertIN = f'{IN:_.2f}'
            IN = convertIN.replace('.', ',').replace('_', '.')

            convertIR = f'{IR:_.2f}'
            IR = convertIR.replace('.', ',').replace('_', '.')

            convertIS = f'{IS:_.2f}'
            IS = convertIS.replace('.', ',').replace('_', '.')

            baseCS = valorNF

            convertBaseIN = fValorNF * (50 / 100)
            baseIN = f'{convertBaseIN:_.2f}'
            baseIN = baseIN.replace('.', ',').replace('_', '.')

            baseIR = valorNF

            convertBaseIS = fValorNF * (50 / 100)
            baseIS = f'{convertBaseIS:_.2f}'
            baseIS = baseIS.replace('.', ',').replace('_', '.')

            janela['codImp1'].update('CS:')
            janela['base1'].update(baseCS)
            janela['valor1'].update(CS)
            janela['codImp2'].update('IN:')
            janela['base2'].update(baseIN)
            janela['valor2'].update(IN)
            janela['codImp3'].update('IR:')
            janela['base3'].update(baseIR)
            janela['valor3'].update(IR)
            janela['codImp4'].update('IS:')
            janela['base4'].update(baseIS)
            janela['valor4'].update(IS)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')
            janela['dedValor'].update(fValorNF * 50 /100)
            janela['inssDed'].update(50)
            janela['aliqISS'].update("5.00")

            IN = INReturn
            IR = IRReturn
            IS = ISReturn

      # Se o evento for clicar no botão INSS, então:
      if evento == 'INSS':
            limparConsulta()
            IN = (fValorNF * (INDed / 100)) * IN

            valorLiq = fValorNF - IN
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertIN = f'{IN:_.2f}'
            IN = convertIN.replace('.', ',').replace('_', '.')

            baseIN = fValorNF * (INDed / 100)
            convertBaseIN = f'{baseIN:_.2f}'
            baseIN = convertBaseIN.replace('.', ',').replace('_', '.')

            janela['codImp1'].update('INSS:')
            janela['base1'].update(baseIN)
            janela['valor1'].update(IN)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')

            IN = INReturn



      # Se o evento for clicar no botão PCC/IN/IR, então:
      if evento == 'PCC/IN/IR':
            limparConsulta()
            PCC = fValorNF * (4.65 / 100)
            IN = (fValorNF * (INDed / 100)) * IN
            IR = fValorNF * (IR)

            valorLiq = fValorNF - PCC - IN - IR
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertPCC = f'{PCC:_.2f}'
            PCC = convertPCC.replace('.', ',').replace('_', '.')

            convertIN = f'{IN:_.2f}'
            IN = convertIN.replace('.', ',').replace('_', '.')

            convertIR = f'{IR:_.2f}'
            IR = convertIR.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            basePCC = valorNF

            convertBaseIN = fValorNF * (INDed / 100)
            baseIN = f'{convertBaseIN:_.2f}'
            baseIN = baseIN.replace('.', ',').replace('_', '.')

            baseIR = valorNF

            janela['codImp1'].update('PCC:')
            janela['base1'].update(basePCC)
            janela['valor1'].update(PCC)
            janela['codImp2'].update('IN:')
            janela['base2'].update(baseIN)
            janela['valor2'].update(IN)
            janela['codImp3'].update('IR:')
            janela['base3'].update(baseIR)
            janela['valor3'].update(IR)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')

            IR = IRReturn
            IN = INReturn



      # Se o evento for clicar no botão IN/IS, então:
      if evento == 'IN/IS':
            limparConsulta()
            IN = (fValorNF * (INDed / 100)) * IN
            IS = (fValorNF - ISDed) * IS / 100

            valorLiq = fValorNF - IN - IS
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertIN = f'{IN:_.2f}'
            IN = convertIN.replace('.', ',').replace('_', '.')

            convertIS = f'{IS:_.2f}'
            IS = convertIS.replace('.', ',').replace('_', '.')

            baseIN = fValorNF * (INDed / 100)
            convertBaseIN = f'{baseIN:_.2f}'
            baseIN = convertBaseIN.replace('.', ',').replace('_', '.')

            baseIS = fValorNF - ISDed
            convertBaseIS = f'{baseIS:_.2f}'
            baseIS = convertBaseIS.replace('.', ',').replace('_', '.')

            janela['codImp1'].update('IN:')
            janela['base1'].update(baseIN)
            janela['valor1'].update(IN)
            janela['codImp2'].update('IS:')
            janela['base2'].update(baseIS)
            janela['valor2'].update(IS)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')

            IS = ISReturn
            IN = INReturn



      # Se o evento for clicar no botão IR, então:
      if evento == 'IR':
            limparConsulta()
            IR = fValorNF * (IR)

            valorLiq = fValorNF - IR
            convertValorLiq = f'{valorLiq:_.2f}'
            valorLiq = convertValorLiq.replace('.', ',').replace('_', '.')

            convertIR = f'{IR:_.2f}'
            IR = convertIR.replace('.', ',').replace('_', '.')

            valorNF = f'{fValorNF:_.2f}'
            valorNF = valorNF.replace('.', ',').replace('_', '.')

            baseIR = valorNF

            janela['codImp1'].update('IR:')
            janela['base1'].update(baseIR)
            janela['valor1'].update(IR)
            janela['valorLiquido'].update(f'O valor líquido é: {valorLiq}')

            IR = IRReturn


      #Se clicar no botão Copiar Valores:
      if evento == 'Copiar Valores':
            #Seta nas variáveis abaixo os valores que estão nos campos
            base1 = valores['base1']
            valor1 = valores['valor1']
            base2 = valores['base2']
            valor2 = valores['valor2']
            base3 = valores['base3']
            valor3 = valores['valor3']
            base4 = valores['base4']
            valor4 = valores['valor4']
            codImp1 = valores['codImp1']
            codImp2 = valores['codImp2']
            codImp3 = valores['codImp3']
            codImp4 = valores['codImp4']

            #Cria um dataframe com base nas variáveis acima
            df1 = pd.DataFrame([[base2, valor2], [base3, valor3], [base4, valor4]],
                               index=['1', '2', '3'],
                               columns=[base1, valor1])

            #Cria um excel com os valores acima
            df1.to_excel("CopiarValores.xlsx")

            #Copia os valores do excel
            df1.to_clipboard(excel=True, index=False)

            #Deleta o arquivo excel
            os.remove('CopiarValores.xlsx')

janela.close()







