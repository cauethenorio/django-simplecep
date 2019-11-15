import typescript from 'rollup-plugin-typescript2';
import {terser} from "rollup-plugin-terser";


export default (commandLineArgs) => {
    const debug = commandLineArgs.configDebug === true;

    return ({
        input: 'src/index.ts',
        output: {
            file: '../simplecep/static/simplecep/simplecep-autofill.js',
            format: 'iife',
            name: 'SimplecepAutofill',
        },
        plugins: [
            typescript({
                typescript: require('typescript'),
            }),
            debug? undefined : terser()
        ]
    });
}
