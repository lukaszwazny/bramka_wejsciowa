import * as React from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import ReactHtmlParser from 'react-html-parser';
import { readFileSync } from 'fs';

export interface IState {
    value: string | undefined;
    Items: ComponentFramework.PropertyTypes.DataSet | null;
}

export interface IProps {
    value: string | undefined;
    Items: ComponentFramework.PropertyTypes.DataSet | null;
    onChange: (value:string, Items : ComponentFramework.PropertyTypes.DataSet) => void;
}

export default class ReactSampleTextBox extends React.Component<IProps, IState> {

    selectedRecord: any

    constructor(props: Readonly<IProps>){
        super(props);
        this.state = { value: props.value, Items: props.Items };
        //this.state = { value: props.value };
        this.handleChange = this.handleChange.bind(this); 
    }

    componentWillReceiveProps(p: IProps) {
        console.log(p.Items);
        this.setState({value: (p.value), Items: (p.Items)});
    }

    handleChange(e:string){
        let value = e;
        this.setState({value: (value)});
        this.props.onChange(value, this.state.Items as ComponentFramework.PropertyTypes.DataSet);
    }

    private typesDict : {[k: string]: any} = {
        'DateAndTime.DateAndTime': 'date',
        'Decimal': 'numeric'
    }


    render() {

        let data:any[] = [];
        this.state.Items?.sortedRecordIds.forEach( id => {
            let record: {[k: string]: any} = {};
            this.state.Items?.columns.forEach(col => {
                let recValue : any = this.state.Items?.records[id].getValue(col.alias)
                if (recValue instanceof Date) {
                    let temp : Date = recValue as Date
                    recValue = temp?.toISOString().slice(0,10)
                    col.dataType = "DateAndTime.DateAndTime"
                }
                else if (/^\d{4}-([0]\d|1[0-2])-([0-2]\d|3[01])$/.test(recValue as string)) {
                    col.dataType = "DateAndTime.DateAndTime"
                }
                else if (!isNaN(recValue) && !isNaN(parseFloat(recValue))) {
                    col.dataType = "Decimal"
                }
                else{
                    recValue = recValue
                }
                record[col.alias.toLowerCase()] = recValue;
                //data.push(this.state.Items?.records[id].getValue(col.alias));
            });
            data.push(record);
        });
        
        console.log(data);
        
        // 
        const dynamicColumns = this.state.Items?.columns.map((col,i) => {
            if (col.alias != "id")
                return <Column dataType={((col.dataType in this.typesDict) ? this.typesDict[col.dataType] : "text")} key={col.alias.toLowerCase()} sortable field={col.alias.toLowerCase()} header={col.alias} filter/>;
        });

        // const colm = <Column field="data" header="DATA" filter/>
        // let siema = "data"
        // let halo = this.state.Items!.columns[0].name.toLowerCase().valueOf().normalize()
        // console.log("siema 0:",siema.charCodeAt(0))
        // console.log("siema 1:",siema.charCodeAt(1))
        // console.log("siema 2:",siema.charCodeAt(2))
        // console.log("siema 3:",siema.charCodeAt(3))
        // console.log("halo 0:", halo.charCodeAt(0))
        // console.log("halo 1:", halo.charCodeAt(1))
        // console.log("halo 2:", halo.charCodeAt(2))
        // console.log("halo 3:", halo.charCodeAt(3))
        //const siema = "DATA".toLowerCase()

        //const tab = "<Column field=\"data\" header=\"DATA\" sortable=\"true\" filter=\"true\"/>"
        //console.log("dynamicColumns: ",dynamicColumns)
        // selectionMode={"single"} resizableColumns={true} reorderableColumns={true}
        //{dynamicColumns}
        return (
            <DataTable value={data} 
            selectionMode={"single"} 
            onSelectionChange={e => {this.handleChange(e.value?.id)}} 
            resizableColumns={true} 
            reorderableColumns={true}
            paginator rows={10}> 
                {dynamicColumns}
            </DataTable>
        );
    }
}