import typescript from 'rollup-plugin-typescript2';
import {terser} from "rollup-plugin-terser";


export default {
    input: 'src/index.ts',
    output: {
        file: 'dist/bundle.js',
        format: 'iife',
        name: 'SimplecepAutofill',
    },
    plugins: [
        typescript({
            typescript: require('typescript'),
        }),
        terser()
    ]
};
