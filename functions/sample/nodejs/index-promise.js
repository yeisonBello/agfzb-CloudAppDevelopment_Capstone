/**
 * Get all dealerships and dealership by id 
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.COUCH_URL);

    const state = params.state;
    if (state) {
        return getAllDealerships(cloudant, "dealerships", state);
    } else {
        return getAllDealerships(cloudant, "dealerships");
    }
}

function getAllDealerships(cloudant, dbname, state) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })
            .then(result => {
                let filteredResults = result.result.rows;
                if (state) {
                    filteredResults = filteredResults.filter(row => {
                        const doc = row.doc;
                        return doc.state === state;
                    });
                }

                if (filteredResults.length === 0) {
                    // Handle no matching state scenario (HTTP 404)
                    reject({ status: 404, message: "The state does not exist" });
                } else {
                    const formattedResults = filteredResults.map(row => {
                        const doc = row.doc;
                        return {
                            id: doc.id,
                            city: doc.city,
                            state: doc.state,
                            st: doc.st,
                            address: doc.address,
                            zip: doc.zip,
                            lat: doc.lat,
                            long: doc.long
                        };
                    });
                    resolve({ result: formattedResults });
                }
            })
            .catch(err => {
                // Handle server error scenario (HTTP 500)
                console.error(err);
                reject({ status: 500, message: "Something went wrong on the server" });
            });
    });
}
