
package us.kbase.kbmsuite;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CheckMInputParams</p>
 * <pre>
 * required params:
 * putative_genomes_folder: folder path that holds all putative genome files with (fa as the file extension) to be checkM-ed
 * checkM_workflow_name: name of the CheckM workflow,e.g., lineage_wf or taxonomy_wf
 * file_extension: the extension of the putative genome file, should be "fna"
 * contig_file: contig file path/shock_id in File structure
 * out_header: output file header
 * workspace_name: the name of the workspace it gets saved to.
 * semi-required: at least one of the following parameters is needed
 * abund_list: contig abundance file(s)/shock_id(s)
 * reads_list: reads file(s)/shock_id(s) in fasta or fastq format
 * optional params:
 * thread: number of threads; default 1
 * external_genes: indicating an external gene call instead of using prodigal, default 0
 * external_genes_file: the file containing genes for gene call, default "" 
 * reassembly: specify this option if you want to reassemble the bins.
 *             note that at least one reads file needs to be designated.
 * prob_threshold: minimum probability for EM algorithm; default 0.8
 * markerset: choose between 107 marker genes by default or 40 marker genes
 * min_contig_length: minimum contig length; default 1000
 * plotmarker: specify this option if you want to plot the markers in each contig
 * ref: https://github.com/Ecogenomics/CheckM/wiki/Installation#how-to-install-checkm
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "checkM_workflow_name",
    "putative_genomes_folder",
    "file_extension",
    "workspace_name",
    "thread",
    "external_genes",
    "external_genes_file",
    "reassembly",
    "prob_threshold",
    "markerset",
    "min_contig_length",
    "plotmarker"
})
public class CheckMInputParams {

    @JsonProperty("checkM_workflow_name")
    private String checkMWorkflowName;
    @JsonProperty("putative_genomes_folder")
    private String putativeGenomesFolder;
    @JsonProperty("file_extension")
    private String fileExtension;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("thread")
    private Long thread;
    @JsonProperty("external_genes")
    private Long externalGenes;
    @JsonProperty("external_genes_file")
    private String externalGenesFile;
    @JsonProperty("reassembly")
    private Long reassembly;
    @JsonProperty("prob_threshold")
    private Double probThreshold;
    @JsonProperty("markerset")
    private Long markerset;
    @JsonProperty("min_contig_length")
    private Long minContigLength;
    @JsonProperty("plotmarker")
    private Long plotmarker;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("checkM_workflow_name")
    public String getCheckMWorkflowName() {
        return checkMWorkflowName;
    }

    @JsonProperty("checkM_workflow_name")
    public void setCheckMWorkflowName(String checkMWorkflowName) {
        this.checkMWorkflowName = checkMWorkflowName;
    }

    public CheckMInputParams withCheckMWorkflowName(String checkMWorkflowName) {
        this.checkMWorkflowName = checkMWorkflowName;
        return this;
    }

    @JsonProperty("putative_genomes_folder")
    public String getPutativeGenomesFolder() {
        return putativeGenomesFolder;
    }

    @JsonProperty("putative_genomes_folder")
    public void setPutativeGenomesFolder(String putativeGenomesFolder) {
        this.putativeGenomesFolder = putativeGenomesFolder;
    }

    public CheckMInputParams withPutativeGenomesFolder(String putativeGenomesFolder) {
        this.putativeGenomesFolder = putativeGenomesFolder;
        return this;
    }

    @JsonProperty("file_extension")
    public String getFileExtension() {
        return fileExtension;
    }

    @JsonProperty("file_extension")
    public void setFileExtension(String fileExtension) {
        this.fileExtension = fileExtension;
    }

    public CheckMInputParams withFileExtension(String fileExtension) {
        this.fileExtension = fileExtension;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public CheckMInputParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("thread")
    public Long getThread() {
        return thread;
    }

    @JsonProperty("thread")
    public void setThread(Long thread) {
        this.thread = thread;
    }

    public CheckMInputParams withThread(Long thread) {
        this.thread = thread;
        return this;
    }

    @JsonProperty("external_genes")
    public Long getExternalGenes() {
        return externalGenes;
    }

    @JsonProperty("external_genes")
    public void setExternalGenes(Long externalGenes) {
        this.externalGenes = externalGenes;
    }

    public CheckMInputParams withExternalGenes(Long externalGenes) {
        this.externalGenes = externalGenes;
        return this;
    }

    @JsonProperty("external_genes_file")
    public String getExternalGenesFile() {
        return externalGenesFile;
    }

    @JsonProperty("external_genes_file")
    public void setExternalGenesFile(String externalGenesFile) {
        this.externalGenesFile = externalGenesFile;
    }

    public CheckMInputParams withExternalGenesFile(String externalGenesFile) {
        this.externalGenesFile = externalGenesFile;
        return this;
    }

    @JsonProperty("reassembly")
    public Long getReassembly() {
        return reassembly;
    }

    @JsonProperty("reassembly")
    public void setReassembly(Long reassembly) {
        this.reassembly = reassembly;
    }

    public CheckMInputParams withReassembly(Long reassembly) {
        this.reassembly = reassembly;
        return this;
    }

    @JsonProperty("prob_threshold")
    public Double getProbThreshold() {
        return probThreshold;
    }

    @JsonProperty("prob_threshold")
    public void setProbThreshold(Double probThreshold) {
        this.probThreshold = probThreshold;
    }

    public CheckMInputParams withProbThreshold(Double probThreshold) {
        this.probThreshold = probThreshold;
        return this;
    }

    @JsonProperty("markerset")
    public Long getMarkerset() {
        return markerset;
    }

    @JsonProperty("markerset")
    public void setMarkerset(Long markerset) {
        this.markerset = markerset;
    }

    public CheckMInputParams withMarkerset(Long markerset) {
        this.markerset = markerset;
        return this;
    }

    @JsonProperty("min_contig_length")
    public Long getMinContigLength() {
        return minContigLength;
    }

    @JsonProperty("min_contig_length")
    public void setMinContigLength(Long minContigLength) {
        this.minContigLength = minContigLength;
    }

    public CheckMInputParams withMinContigLength(Long minContigLength) {
        this.minContigLength = minContigLength;
        return this;
    }

    @JsonProperty("plotmarker")
    public Long getPlotmarker() {
        return plotmarker;
    }

    @JsonProperty("plotmarker")
    public void setPlotmarker(Long plotmarker) {
        this.plotmarker = plotmarker;
    }

    public CheckMInputParams withPlotmarker(Long plotmarker) {
        this.plotmarker = plotmarker;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((((((((((("CheckMInputParams"+" [checkMWorkflowName=")+ checkMWorkflowName)+", putativeGenomesFolder=")+ putativeGenomesFolder)+", fileExtension=")+ fileExtension)+", workspaceName=")+ workspaceName)+", thread=")+ thread)+", externalGenes=")+ externalGenes)+", externalGenesFile=")+ externalGenesFile)+", reassembly=")+ reassembly)+", probThreshold=")+ probThreshold)+", markerset=")+ markerset)+", minContigLength=")+ minContigLength)+", plotmarker=")+ plotmarker)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
