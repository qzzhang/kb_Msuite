
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
 * bin_folder: folder path that holds all putative genome files with (fa as the file extension) to be checkM-ed
 * out_folder: folder path that holds all putative genome files with (fa as the file extension) to be checkM-ed
 * checkM_cmd_name: name of the CheckM workflow,e.g., lineage_wf or taxonomy_wf
 * workspace_name: the name of the workspace it gets saved to.
 * optional params:
 * file_extension: the extension of the putative genome file, should be "fna"
 * thread: number of threads; default 1
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "bin_folder",
    "out_folder",
    "checkM_cmd_name",
    "workspace_name",
    "file_extension",
    "thread"
})
public class CheckMInputParams {

    @JsonProperty("bin_folder")
    private String binFolder;
    @JsonProperty("out_folder")
    private String outFolder;
    @JsonProperty("checkM_cmd_name")
    private String checkMCmdName;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("file_extension")
    private String fileExtension;
    @JsonProperty("thread")
    private Long thread;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("bin_folder")
    public String getBinFolder() {
        return binFolder;
    }

    @JsonProperty("bin_folder")
    public void setBinFolder(String binFolder) {
        this.binFolder = binFolder;
    }

    public CheckMInputParams withBinFolder(String binFolder) {
        this.binFolder = binFolder;
        return this;
    }

    @JsonProperty("out_folder")
    public String getOutFolder() {
        return outFolder;
    }

    @JsonProperty("out_folder")
    public void setOutFolder(String outFolder) {
        this.outFolder = outFolder;
    }

    public CheckMInputParams withOutFolder(String outFolder) {
        this.outFolder = outFolder;
        return this;
    }

    @JsonProperty("checkM_cmd_name")
    public String getCheckMCmdName() {
        return checkMCmdName;
    }

    @JsonProperty("checkM_cmd_name")
    public void setCheckMCmdName(String checkMCmdName) {
        this.checkMCmdName = checkMCmdName;
    }

    public CheckMInputParams withCheckMCmdName(String checkMCmdName) {
        this.checkMCmdName = checkMCmdName;
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
        return ((((((((((((((("CheckMInputParams"+" [binFolder=")+ binFolder)+", outFolder=")+ outFolder)+", checkMCmdName=")+ checkMCmdName)+", workspaceName=")+ workspaceName)+", fileExtension=")+ fileExtension)+", thread=")+ thread)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
