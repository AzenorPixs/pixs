// Profil AST des octets propriétaires réellement présents, budgets explicites de recette.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {analyzePresentationSource} from '../scripts/presentation-profile-v1.mjs';

for(const owner of ['pzt','dns']){
  test('C14 profil source : '+owner+' sans acces hors presentation',async()=>{
    const source=await readFile(new URL('../../src/pixs/'+owner+'/frontend.mjs',import.meta.url),'utf8');
    const result=analyzePresentationSource(source,{
      maxSourceBytes:65536,maxAstNodes:16384,maxBindings:1024,maxTextLength:4096,maxScopeDepth:64});
    assert.equal(result.schema,'pixs.presentation.source-profile/1.0.0');
    assert.ok(result.ast_nodes>0);
    console.log(JSON.stringify({owner:'pixs.'+owner,sha256:createHash('sha256').update(source).digest('hex'),...result}));
  });
}
