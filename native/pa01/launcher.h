/* Interface de liaison PA01 : table générée exclusivement depuis le build. */
#ifndef PIXS_PA01_LAUNCHER_H
#define PIXS_PA01_LAUNCHER_H
#define PY_SSIZE_T_CLEAN
#include <Python.h>

struct pa01_embedded_program {
    unsigned int schema_version;
    const char *executable;
    const char *entry_module;
    struct _inittab *modules;
};

/* Définition fournie par le générateur, liée aux objets réellement produits. */
extern const struct pa01_embedded_program pa01_program;
#endif
