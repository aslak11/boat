import React from 'react';
import axios from 'axios';
import MaterialTable from 'material-table';

import PropTypes, {func} from 'prop-types';
import clsx from 'clsx';
import {makeStyles, withStyles} from '@material-ui/core/styles';
import TableCell from '@material-ui/core/TableCell';
import Paper from '@material-ui/core/Paper';
import {AutoSizer, Column, Table} from 'react-virtualized';
import {PhotoCamera} from "@material-ui/icons";
import IconButton from "@material-ui/core/IconButton";
import Button from "@material-ui/core/Button";
import CircularProgress from "@material-ui/core/CircularProgress";
import {fade} from "@material-ui/core";
import LoadingOverlay from 'react-loading-overlay';
import Typography from "@material-ui/core/Typography";
import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";

const useStyles = makeStyles((theme) => ({
    root: {
        '& > *': {
            margin: theme.spacing(1),
        },
    },
    input: {
        display: 'none',
    },
}));

function UploadButton(props) {
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <input
                accept="text/csv"
                className={classes.input}
                id="contained-button-file"
                onChange={(e) => {
                    if (e.target.files && e.target.files.length > 0) {
                        props.upload(e.target.files[0]);
                    }
                }}
                type="file"
            />
            <label htmlFor="contained-button-file">
                <Button variant="contained" color="primary" component="span">
                    Upload
                </Button>
            </label>
        </div>
    );
}

const AlertDialog = props => (
    <div>
        <Dialog
            open={props.open}
            onClose={props.onClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
        >
            <DialogTitle id="alert-dialog-title">{props.title}</DialogTitle>
            <DialogContent>
                <DialogContentText id="alert-dialog-description">
                    {props.description}
                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <Button onClick={props.onClose} color="primary">
                    {props.close}
                </Button>
                <Button onClick={props.onConfirm} color="primary" autoFocus>
                    {props.confirm}
                </Button>
            </DialogActions>
        </Dialog>
    </div>
);

const url = process.env.REACT_APP_API_URL || "http://localhost:5000"


class App extends React.Component {
    state = {
        data: [],
        loading: false,
        error: "",
        alertDialog: {
            open: false,
            description: "",
            data: []
        }
    }

    componentDidMount() {
        this.update1()
    }

    handleDialogClose = () => {
        this.setState({...this.state, alertDialog: {...this.state.alertDialog, open: false}});
    }

    handleDialogConfirm = () => {
        const rows = Array.from(this.state.alertDialog.data, x => x.mmsi);
        this.setState({...this.state, loading: true, alertDialog: {...this.state.alertDialog, open: false}});
        axios.delete(url + "/api/list", {data: rows}).then(response => {
            this.setState({...this.state, loading: false});
            this.update1();
        })
    }

    update1 = () => {
        this.setState({...this.state, loading: true})
        axios.get(url + '/api/get_vessel').then(response => {
            this.setState({...this.state, data: response.data, loading: false})
        }).catch(error => {
            this.setState({...this.state, error: error.response.statusText, loading: false})
            console.log(this.state.error)
        });
    }

    upload = (file) => {
        this.setState({...this.state, loading: true});
        const formData = new FormData();
        formData.append('file', file);

        axios.post(url + '/api/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }).then(response => {
            this.setState({...this.state, loading: false});
            this.update1();
        }).catch(error => {
            this.setState({...this.state, error: error.response.statusText, loading: false})
            console.log(this.state.error)
        });
    }

    deleteRows = (evt, data) => {
        console.log(this.state)
        this.setState({
            ...this.state,
            alertDialog: {
                ...this.state.alertDialog,
                open: true,
                description: 'You want to delete ' + data.length + ' rows',
                data: data,
            }
        });
    }

    render() {
        console.log(this.state.loading)

        return (
            <div>
                <LoadingOverlay
                    active={this.state.loading}
                    spinner
                    text='Loading your content...'
                >
                    <div style={{marginLeft: 2, marginTop: 10}}>
                        <UploadButton upload={this.upload}/>
                    </div>
                    <div style={{margin: 10}}>
                        <MaterialTable
                            title={""}
                            options={{
                                selection: true
                            }}
                            columns={[
                                {title: 'mmsi', field: 'mmsi', type: 'numeric'},
                                {title: 'imo', field: 'imo', type: 'numeric'},
                                {title: 'name', field: 'name'},
                                {title: 'type', field: 'type'}
                            ]}

                            data={this.state.data}
                            actions={[
                                {
                                    icon: 'refresh',
                                    tooltip: 'Refresh Data',
                                    isFreeAction: true,
                                    onClick: () => this.update1(),
                                },
                                {
                                    tooltip: 'Remove All Selected Users',
                                    icon: 'delete',
                                    onClick: this.deleteRows
                                }
                            ]}
                        />
                        <Typography style={{margin: 10, marginLeft: 1}} color={"error"}>{this.state.error}</Typography>
                    </div>
                </LoadingOverlay>
                <AlertDialog open={this.state.alertDialog.open} close={"No"} confirm={"Yes"}
                             description={this.state.alertDialog.description} onClose={this.handleDialogClose}
                             onConfirm={this.handleDialogConfirm}/>
            </div>
        );
    }
}

export default App;
