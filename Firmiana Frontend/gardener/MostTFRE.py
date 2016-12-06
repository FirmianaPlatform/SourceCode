import gardener.models
import experiments.models
import operator
import math
from scipy.stats import pearsonr,ttest_ind
organ = 'stomach'
base_dir = '/usr/local/firmiana/data/mostTF/GC/'
# exps = gardener.models.Experiment.objects.filter(bait='TFRE;').filter(
#    description__icontains=organ).filter(stage=5).filter(is_deleted=0).filter(species__icontains='homo')


def getExps():
    pairwiseExp = []
    f = open(base_dir + 'lung_files.txt', 'U')
    for line in f:
        if line.strip() == '':
            continue
        word = line.strip().split(' ')
        print word
        tumor = 'Exp' + word[0].split(':')[1]
        normal = 'Exp' + word[1].split(':')[1]
        pairwiseExp.append((tumor, normal))
    return pairwiseExp


def getExpGC():
    pairwiseExp = []
    title = 'Exp001462*Exp001461*Exp001460*Exp001459*Exp001458*Exp001457*Exp001456*Exp001455*Exp001454*Exp001453*Exp001452*Exp001451*Exp001450*Exp001449*Exp001448*Exp001447*Exp001446*Exp001445*Exp001444*Exp001443*Exp001442*Exp001441*Exp001440*Exp001439*Exp001438*Exp001437*Exp001436*Exp001435*Exp001434*Exp001433*Exp001432*Exp001431*Exp001430*Exp001429*Exp001428*Exp001427*Exp001426*Exp001425*Exp001423*Exp001424*Exp001265*Exp001263*Exp001264*Exp001262*Exp001261*Exp001260*Exp001259*Exp001258*Exp001257*Exp001256*Exp001255*Exp001254*Exp001253*Exp001252*Exp001251*Exp001250*Exp001249*Exp001248*Exp001247*Exp001246*Exp001245*Exp001244*Exp001243*Exp001242*Exp001241*Exp001240*Exp001239*Exp001238*Exp001237*Exp001236*Exp001235*Exp001234*Exp001233*Exp001232*Exp001231*Exp001230*Exp001229*Exp001228*Exp001227*Exp001226*Exp001225*Exp001223*Exp001224*Exp001222*Exp001051*Exp001050*Exp001049*Exp001048*Exp001047*Exp001046*Exp001045*Exp001044*Exp000932*Exp000931*Exp000930*Exp000929*Exp000928*Exp000927*Exp000926*Exp000925*Exp000924*Exp000923*Exp000922*Exp000921*Exp000920*Exp000919*Exp000918*Exp000917*Exp000898*Exp000897*Exp000896*Exp000895*Exp000894*Exp000893*Exp000892*Exp000891*Exp000801*Exp000799*Exp000800*Exp000798*Exp000797*Exp000796*Exp000795*Exp000794*Exp000793*Exp000792*Exp000791*Exp000790*Exp000789*Exp000788*Exp000787*Exp000786*Exp000718*Exp000717*Exp000545*Exp000544*Exp000543*Exp000542*Exp000541*Exp000540'
    gc = title.split('*')
    # print gc
    gc = sorted(gc)
    # print gc
    for i in range(0, len(gc), 2):
        pairwiseExp.append((gc[i], gc[i + 1]))
    return pairwiseExp


def getProteins():
    for exp in exps:
        if 'P' in exp.description:
            f = open(base_dir + exp.name + '_P.txt', 'w')
        else:
            f = open(base_dir + exp.name + '_T.txt', 'w')
        f.write('accession\tsymbol\tibaq\tfot\tnum_peptides\tnum_uni_peptides\n')
        proteins = gardener.models.Exp_Protein.objects.filter(search__exp=exp).filter(
            search__type='exp').filter(type=1).filter(num_peptides__gt=1).filter(
            annotation__icontains='tf_1')
        total_ibaq = 0
        for protein in proteins:
            total_ibaq += protein.ibaq
        for protein in proteins:
            f.write(protein.accession + '\t' + protein.symbol + '\t' + str(protein.ibaq /
                                                                           total_ibaq) + '\t' + str(protein.num_peptides) + '\t' + str(protein.num_uni_peptides) + '\n')
        f.close()


def getGenes(pairwiseExp):
    def calc_percentile(a, small, big):
        if a == 0:
            return int(math.log(big / small, 3))
        return int(math.log(big / small, 3)) - int(math.log(a / small, 3))+1
    for pairs in pairwiseExp:
        for experiment in pairs:
            exp = gardener.models.Experiment.objects.get(name=experiment)
            print exp.name, exp.description
            if '(T)' in exp.description:
                f = open(base_dir + exp.name + '_T.txt', 'w')
            else:
                f = open(base_dir + exp.name + '_P.txt', 'w')
            f.write('symbol\tibaq\tfot\tnum_peptides\tnum_uni_peptides\tRank\n')
            genes = gardener.models.Exp_Gene.objects.filter(search__exp=exp).filter(type=1).filter(num_peptides__gt=1).filter(
                annotation__icontains='tf_1')
            total_ibaq = 0
            big = 0
            small = 1e15
            for gene in genes:
                total_ibaq += gene.ibaq
                big = max(big, gene.ibaq)
                if gene.ibaq > 0:
                    small = min(small, gene.ibaq)
            genes = genes.order_by('-ibaq')
            i = 0
            total = len(genes)
            for gene in genes:
                f.write(gene.symbol + '\t' + str(gene.ibaq) + '\t' + str(gene.ibaq / total_ibaq) +
                        '\t' + str(gene.num_peptides) + '\t' + str(gene.num_uni_peptides) + '\t' + str(calc_percentile(gene.ibaq, small,big)) + '\n')
                i = i + 1
            f.close()
    print big, small


def get50(pairwiseExp):
    symbols = {}
    #===========================================================================
    # exp_name = []
    # for exp in exps:
    #     if 'P' in exp.description:
    #         exp_name.append(exp.name + '_P.txt')
    #     else:
    #         exp_name.append(exp.name + '_T.txt')
    # exp_name = sorted(exp_name)
    #===========================================================================
    up50 = {}
    down50 = {}
    for pairexp in pairwiseExp:
        exp1 = pairexp[0] + '_T.txt'
        exp2 = pairexp[1] + '_P.txt'
        gene1 = {}
        gene2 = {}
        f = open(base_dir + exp1, 'U')
        for line in f:
            if 'symbol' in line:
                continue
            word = line.split('\t')
            gene1[word[0]] = float(word[1])
            if word[0] not in symbols:
                symbols[word[0]] = 70
        f.close()
        f = open(base_dir + exp2, 'U')
        for line in f:
            if 'symbol' in line:
                continue
            word = line.split('\t')
            gene2[word[0]] = float(word[1])
            if word[0] not in symbols:
                symbols[word[0]] = 70
        f.close()
        upratio = {}
        downratio = {}
        for pro in gene1:
            if pro in gene2 and gene2[pro] != 0:
                upratio[pro] = gene1[pro] / gene2[pro]
            else:
                upratio[pro] = 1e9
        sorted_up = sorted(
            upratio.items(), key=operator.itemgetter(1), reverse=True)
        for pro in sorted_up:
            if pro[0] not in up50:
                up50[pro[0]] = 0
            if pro[1] > 10:
                up50[pro[0]] += 1
        for pro in gene2:
            if pro in gene1 and gene1[pro] != 0:
                downratio[pro] = gene2[pro] / gene1[pro]
            else:
                downratio[pro] = 1e9
        sorted_down = sorted(
            downratio.items(), key=operator.itemgetter(1), reverse=True)
        for pro in sorted_down:
            if pro[0] not in down50:
                down50[pro[0]] = 0
            if pro[1] > 3:
                down50[pro[0]] += 1
        for pro in symbols:
            if (pro not in gene1) and (pro not in gene2):
                symbols[pro] -= 1
    f = open(base_dir + organ + '_up.txt', 'w')
    f.write('Symbol\tNo.\n')
    for pro in up50:
        f.write(pro + '\t' + str(up50[pro]) + '\n')
    f.close()
    f = open(base_dir + organ + '_down.txt', 'w')
    f.write('Symbol\tNo.\n')
    for pro in down50:
        f.write(pro + '\t' + str(down50[pro]) + '\n')
    f.close()
    f = open(base_dir + organ + '_up&down.txt', 'w')
    f.write('Symbol\tUp_No.\tDown_No.\tothers\n')
    for pro in symbols:
        f.write(pro + '\t')
        up = up50[pro] if pro in up50 else 0
        down = down50[pro] if pro in down50 else 0
        f.write(str(up) + '\t' + str(down) + '\t' +
                str(symbols[pro] - up - down) + '\n')
    f.close()


def getGC(pairwiseExp):
    def change(a):
        small=1e100
        for pp in a:
            if pp>0:
                small=min(small,pp)
        return [math.log(x) if x >0 else math.log(small) for x in a]
    def changenew(a,b):
        j=0
        a_new=[]
        b_new=[]
        for i in range(len(a)):
            if a[i]<0.1 and b[i]<0.1:
                a_new.append(a[i])
                b_new.append(b[i])
            else:
                j=j+1
        print j
        return a_new,b_new
    symbols = set()
    f1 = open(base_dir + 'all.txt', 'w')
    for pairexp in pairwiseExp:
        exp1 = pairexp[0] + '_T.txt'
        exp2 = pairexp[1] + '_P.txt'
        gene1 = {}
        ibaq1 = {}
        ibaq2 = {}
        gene2 = {}
        rank1 = {}
        rank2 = {}
        smal1=1e9
        smal2=1e9
        f = open(base_dir + exp1, 'U')
        for line in f:
            if 'symbol' in line:
                continue
            word = line.split('\t')
            symbols.add(word[0])
            ibaq1[word[0]] = float(word[1])
            gene1[word[0]] = float(word[2])
            if gene1[word[0]]>0:
                smal1=min(smal1,gene1[word[0]])
            rank1[word[0]] = float(word[-1])
        f.close()
        f = open(base_dir + exp2, 'U')
        for line in f:
            if 'symbol' in line:
                continue
            word = line.split('\t')
            symbols.add(word[0])
            ibaq2[word[0]] = float(word[1])
            gene2[word[0]] = float(word[2])
            if gene2[word[0]]>0:
                smal2=min(smal2,gene2[word[0]])
            rank2[word[0]] = float(word[-1])
        f.close()
        expr1 = []
        expr2 = []
        f = open(base_dir + pairexp[0] + '.txt', 'w')
        f.write('Symbol\tiBaq_T\tifot_T\trank_T\tiBaq_P\tifot_P\trank_P\n')
        for gene in gene1:
            f.write(gene + '\t')
            f.write(str(ibaq1[gene]) + '\t')
            f.write(str(gene1[gene]) + '\t')
            f.write(str(rank1[gene]) + '\t')
            expr1.append(gene1[gene])
            if gene in gene2:
                f.write(str(ibaq2[gene]) + '\t')
                f.write(str(gene2[gene]) + '\t')
                f.write(str(rank2[gene]) + '\n')
                expr2.append(gene2[gene])
            else:
                f.write('0\t0\t')
                f.write('None\n')
                expr2.append(0)
        for gene in gene2:
            if gene not in gene1:
                f.write(gene + '\t')
                f.write('0\t0\tNone\t')
                expr1.append(0)
                f.write(str(ibaq2[gene]) + '\t')
                f.write(str(gene2[gene]) + '\t')
                f.write(str(rank2[gene]) + '\n')
                expr2.append(gene2[gene])
        expr1,expr2=changenew(expr1,expr2)
        f.write('Correlation=\n')
        cor = pearsonr(expr1, expr2)[0]
        f.write(str(cor) + '\n')
        ispec = experiments.models.Experiment.objects.get(
            name=pairexp[0]).fm_no
        f1.write(pairexp[0] + '\t' + str(cor) + '\t' + ispec + '\n')
        f.close()
    f1.close()
    symbols = list(symbols)
    f = open(base_dir + 'list.txt', 'U')
    fout = open(base_dir + 'final.txt', 'w')
    fout.write('\tSymbol' + '\t' + '\t'.join(symbols) + '\n')
    for line in f:
        if 'Firmiana' in line or line.strip() == '':
            continue
        result = open(base_dir + line.strip() + '.txt', 'U').readlines()
        fout.write(line.strip() + '\t' + 'iBaq_T\t')
        for symbol in symbols:
            wri = False
            i = 0
            for newline in result:
                if symbol in newline.split('\t'):
                    wri = True
                    fout.write(newline.strip().split('\t')[1] + '\t')
                    i = i + 1
            if not wri:
                fout.write('NAN\t')
            if i > 1:
                print symbol
        fout.write('\n')
        fout.write(line.strip() + '\t' + 'iFot_T\t')
        for symbol in symbols:
            wri = False
            for newline in result:
                if symbol in newline.split('\t'):
                    wri = True
                    fout.write(newline.strip().split('\t')[2] + '\t')
            if not wri:
                fout.write('NAN\t')
        fout.write('\n')
        fout.write(line.strip() + '\t' + 'rank_T\t')
        for symbol in symbols:
            wri = False
            for newline in result:
                if symbol in newline.split('\t'):
                    wri = True
                    fout.write(newline.strip().split('\t')[3] + '\t')
            if not wri:
                fout.write('NAN\t')
        fout.write('\n')
        fout.write(line.strip() + '\t' + 'iBaq_P\t')
        for symbol in symbols:
            wri = False
            for newline in result:
                if symbol in newline.split('\t'):
                    wri = True
                    fout.write(newline.strip().split('\t')[4] + '\t')
            if not wri:
                fout.write('NAN\t')
        fout.write('\n')
        fout.write(line.strip() + '\t' + 'iFot_P\t')
        for symbol in symbols:
            wri = False
            for newline in result:
                if symbol in newline.split('\t'):
                    wri = True
                    fout.write(newline.strip().split('\t')[5] + '\t')
            if not wri:
                fout.write('NAN\t')
        fout.write('\n')
        fout.write(line.strip() + '\t' + 'rank_p\t')
        for symbol in symbols:
            wri = False
            for newline in result:
                if symbol in newline.split('\t'):
                    wri = True
                    fout.write(newline.strip().split('\t')[6] + '\t')
            if not wri:
                fout.write('NAN\t')
        fout.write('\n')
    fout.close()


def main():
    pairwiseExp = getExps()
    getGenes(pairwiseExp)
    get50(pairwiseExp)

if __name__ == "__main__":
    main()
