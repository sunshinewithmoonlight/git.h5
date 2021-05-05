import sys
import io
import os

while True:
    try:
        from reportlab.platypus import Paragraph, Frame, KeepInFrame, SimpleDocTemplate, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.pagesizes import A4, landscape
        from PyPDF2 import PdfFileWriter, PdfFileReader
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.pdfbase import pdfmetrics
        from googletrans import Translator
        import fitz
        break
    except:
        os.system('pip3 install reportlab PyPDF2 googletrans pymupdf')


def main(argv):

    pdfmetrics.registerFont(TTFont('font_file', 'NotoSansSC-Regular.ttf'))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(fontName='font_file', name='font_fromfile', leading=20*0.9, fontsize=20))

    translator = Translator(service_urls=[r'translate.google.cn'],user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36')

    output = PdfFileWriter()

    filetodo = argv

    if not os.path.isfile(filetodo):
        print('It is not a PDF file. Exit.')
        sys.exit(0)

    pdf = fitz.open(filetodo)


    for page in pdf:
        for xref in page._getContents():
            stream = pdf._getXrefStream(xref)
            #print(pdf._getXrefStream(xref))
            stream = stream.replace(b'Td', b' 3 Tr Td').replace(b' Tm', b' 3 Tr Tm')
            pdf._updateStream(xref, stream)
            #print(pdf._getXrefStream(xref))

    pdf.save(sys.path[0]+'//temp.'+os.path.basename(filetodo))

    temp_empty=open(sys.path[0]+'//temp.'+os.path.basename(filetodo),'rb')
    base_pdf = PdfFileReader(temp_empty)



    i_base_page = 0
    i_translator = 0
    while i_base_page < base_pdf.numPages:
        if_skip_thispage = False

        doc = fitz.open(filetodo)
        doc_page = doc[i_base_page]
        # page.getText("block")
        #print(page.getImageList())
        context = doc_page.getText("blocks")
        # print(context)
        context1 = []
        page_size = doc_page.MediaBox[2:4]
        # print(page_size)

        for elem in context:
            context1.append(elem[4].replace('\n',''))

        context1 = '\n\n\n'.join(context1)



        context2 = []
        count_chars = 0
        i_last = ''
        context1=context1.split('. ')
        for i in context1:
            if len(i_last) < 3500:
                i_last = i_last + i + '. '
                continue
            context2.append(i_last)
            i_translator += 1
            print('Queue %s has chars: %s' %(i_translator, len(i_last)))
            count_chars += len(i_last)
            i_last = '' + i + '. '
            if len(i_last) >= 3500:
                context2.append(i_last)
                i_translator += 1
                print('Queue %s has chars: %s' %(i_translator, len(i_last)))
                count_chars += len(i_last)
                i_last = ''

        i_last=i_last.strip('\n. ')
        context2.append(i_last)
        i_translator += 1
        print('Queue %s has chars: %s' %(i_translator, len(i_last)))
        count_chars += len(i_last)

        print('Current page chars: %s' %count_chars)
        # print(context2)

        if count_chars < 5:
            print('Current page chars are less 5. Skip translate.')
            if_skip_thispage = True



        context3 = []
        for i3 in context2:
            if if_skip_thispage == True:
                context3.append(i3)
            if if_skip_thispage == False:
                while 1:
                    try:
                        context3.append(translator.translate(i3,src='en',dest='zh-cn').text)
                        break
                    except:
                        pass
            # print(context3)

        context3 = ''.join(context3)
        context3 = context3.split('\n\n\n')
        # print(context3)

        # open('4.trans.txt',encoding='UTF8',mode='w').write('\n'.join(context3))
        # context3 = open('4.trans.txt',encoding='UTF8',mode='r').read().split('\n')
        # print(len(context3))


        
        packet = io.BytesIO()
        c = Canvas(packet, pagesize=page_size)
        len_context3 = len(context3)
        i_tran = 0
        while i_tran < len_context3:
            context_i = context[i_tran][:4]
            p0 = context_i[0]
            p1 = page_size[1]-context_i[3]
            # 注意：Frame从下向上绘制，p1=文本框底部位置
            p2 = context_i[2]-context_i[0]
            p3 = context_i[3]-context_i[1]
            try:
                story = [Paragraph(context3[i_tran], styles['font_fromfile'])]
            except:
                story = [Paragraph(context3[i_tran].replace(r'&',r'&amp;').replace(r'<',r'&lt;').replace(r'>',r'&gt;'), styles['font_fromfile'])]

            Frame(p0, p1, p2, p3, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0).addFromList([KeepInFrame(0, 0, story)], c)

            #print(context3[i_tran])
            i_tran += 1

        c.save()

        packet.seek(0)
        new_page = PdfFileReader(packet)
        base_page = base_pdf.getPage(i_base_page)
        base_page.mergePage(new_page.getPage(0))
        output.addPage(base_page)
        
        i_base_page += 1

    output.write(open(sys.path[0]+'//trans.'+os.path.basename(filetodo), 'wb'))

    temp_empty.close()
    os.remove(temp_empty.name)


if __name__ == "__main__":
    main(sys.argv[1])
