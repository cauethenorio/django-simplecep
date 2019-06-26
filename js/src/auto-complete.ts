export class SimpleCepAutocomplete {

    options: any;

    constructor(options: any) {
        this.options = options
    }

    cleanCep(cep: string): string {
        return cep.replace('-', '')
    }

    isValid(cep: string): boolean {
        return /^[0-9]{5}[0-9]{3}$/.test(this.cleanCep(cep));
    }

    requestCepData() {
        // var cep = this.cleanCep(this.getCep());
        // return $.get('/registration/cep/' + cep);
    }

    search = (cep: string): void => {
        // this.abortCepDataRequest();
        //
        // if (this.isValid(cep)) {
        //     this.showLoadingIndicator();
        //     this.currentRequest = this.sendCepDataRequest(cep);
        //     this.currentRequest
        //         .then(this.handleCepRequestData, this.handleCepRequestError)
        //         .always(this.hideLoadingIndicator);
        // }
    }
}
