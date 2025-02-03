1) Transfert du fichier avec SCP en utilisant un port spécifié :
    scp -P 22222 level03@localhost:/home/users/level03/level03 .

2) On decompile le binaire, on obtient son code, ici les sécurités STACK CANARY et NX sont actives donc ca limite l'execution de code arbitraire ou corruption de la pile

3) Explication du code :  
    ***Fonction main** :  
        - Elle demande à l'utilisateur de saisir un mot de passe
        - Le mot de passe saisi (input) est passé à la fonction test avec une valeur constante, 322424845
    **Fonction test** :  
        - Elle prend deux arguments : arg1 (le mot de passe utilisateur) et arg2 (la valeur constante 322424845)
        - La fonction calcule la différence entre arg2 et arg1 : diff = arg2 (322424845) - arg1
        - Cette différence est utilisée comme clé pour le déchiffrement XOR dans la fonction decrypt
    **Fonction decrypt** :  
        - Elle utilise le dechiffrement XOR. Le déchiffrement XOR est une méthode de cryptographie symétrique qui utilise l'opération logique "exclusive OR" (XOR) pour transformer les données
        - Elle reçoit la clé calculée par la fonction test.
        - Utilise cette clé pour déchiffrer une chaîne codée statique "Q}|u\sfg~sf{}|a3"` via une opération XOR caractère par caractère.
        - Après déchiffrement, la chaîne résultante est comparée à "Congratulations!".
        - Si la chaîne déchiffrée correspond à "Congratulations!", alors la fonction decrypt ouvre un shell (via system("/bin/sh")). Sinon, elle affiche "Invalid Password".

4) Déchiffrement :  
    Comme la fonction `decrypt` utilise une méthode de chiffrement symétrique, l'objectif ici est de trouver la clé de déchiffrement.  
    On sait que la chaîne encodée est `Q}|u\sfg~sf{}|a3` et que le résultat souhaité est `"Congratulations!"`.  
    Le XOR est réversible, c'est-à-dire que si on a deux bits A et B et qu'on les combine avec XOR, on peut obtenir C :  
    C = A XOR B.  
    Ainsi, si l'on connaît B et C, on peut retrouver A.  

    Dans notre cas :  
    - A est la clé que nous recherchons,  
    - B est la lettre `Q` de `Q}|u\sfg~sf{}|a3`,  
    - C est la lettre `C` de `"Congratulations!"`.  

    Ainsi, nous obtenons :  
        Key = Q XOR C = 18  
        on peut écrire un petit programme pour vérifier :  
```C
#include <stdio.h>
#include <string.h>

int main() {
    char encoded[] = "Q}|u`sfg~sf{}|a3";
    char target[] = "Congratulations!";
    int key = target[0] ^ encoded[0]; // 'C' ^ 'Q'

    for (int i = 0; i < strlen(encoded); i++) {
        encoded[i] ^= key;
    }
    if (strcmp(encoded, target) == 0)
        printf("Key %d decrypts the encoded string to 'Congratulations!'\n", key);
    else
        printf("Key %d does not decrypt correctly.\n", key);
}
```

5) Trouver le password : 
    Maintenant qu'on sait que la Key est de 18, on fait `322424845 (valeur statique dans le code) - 18 = 322424827`  
    Le password est : `322424827`

```bash
level03@OverRide:~$ ./level03
    ***********************************
    *		level03		**
    ***********************************
    Password:322424827
    $ whoami
    level04
    $ cat /home/users/level04/.pass
    kgv3tkEb9h2mLkRsPkXRfc2mHbjMxQzvb2FrgKkf
```

**Ressources**
    https://en.wikipedia.org/wiki/XOR_cipher
    https://xor.pw/#
